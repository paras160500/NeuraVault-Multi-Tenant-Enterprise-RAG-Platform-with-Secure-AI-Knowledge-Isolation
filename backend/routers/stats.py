#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

from fastapi import APIRouter, Depends
from backend.models.db_models import User,DocumentRecord, UsageStat, StatsOut
from backend.utils.auth import get_current_user
from backend.services.vector_store import VectorStore
from backend.middleware.rate_limiter import rate_limiter

router = APIRouter(prefix="/stats" , tags = ['Stats'])

@router.get("/",response_model=StatsOut)
async def get_status(current_user : User = Depends(get_current_user)):
    """
        Getting the status of the current user from the db 
    """
    # Getting the stats info for particular user 
    stat = await UsageStat.find_one(UsageStat.user_id == current_user.user_id)
    # If we found the stat
    if stat:
        # First if it needed it will reset 
        await stat.reset_daily()

    # Get how many document is ready 
    doc_count = await DocumentRecord.find(
        DocumentRecord.user_id == current_user.user_id,
        DocumentRecord.status == "ready"
    ).count()

    return StatsOut(
        queries_today=stat.queries_today if stat else 0,
        uploads_today=stat.uploads_today if stat else 0,
        total_queries=stat.total_queries if stat else 0,
        total_uploads=stat.total_uploads if stat else 0,
        document_count=doc_count
    )


@router.get("/namespace")
async def get_namespace_stats(current_user : User = Depends(get_current_user)):
    """
        Get the stats of the namespace of the particular user 
    """
    store = VectorStore(namespace=current_user.pinecone_namespace)
    ns_stats = await store.namespace_stats()
    remainig = await rate_limiter.get_query_remaining(current_user.user_id)
    return {
        **ns_stats,
        "queries_remaining_this_minute" : remainig,
        "plan" : current_user.plan 
    }