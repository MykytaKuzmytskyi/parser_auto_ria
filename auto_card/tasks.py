import asyncio
import logging

from asgiref.sync import async_to_sync
from celery import shared_task

from auto_card.pars_manager.processes_script import cards_list
from auto_card.pars_manager.dumps import dumpdata_to_csv

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


@async_to_sync
async def async_pars_cars():
    await cards_list()


@shared_task
def pars_auto_ria():
    async_pars_cars()
    dumpdata_to_csv("data.csv")
