import asyncio

from asgiref.sync import async_to_sync
from django.http import HttpResponse
from pyvirtualdisplay import Display

from auto_card.pars_manager.processes_script import cards_list
from auto_card.pars_manager.dumps import dumpdata_to_csv

loop = asyncio.get_event_loop()


@async_to_sync
async def async_pars_cars():
    display = Display(visible=False, size=(800, 600))
    display.start()
    await cards_list()
    display.stop()


def start_pars(request):
    async_pars_cars()
    dumpdata_to_csv("data.csv")
    return HttpResponse("Data scraping completed.")
