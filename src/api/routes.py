from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from src.processors.pdf_processor import PdfProcessor
from src.sockets.sio import sio_app

router = APIRouter()
pdf_processor = PdfProcessor(max_workers=4, executor_type='thread')

@router.post("/process-pdf/")
async def process_pdf_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    background_tasks.add_task(pdf_processor.process_pdf, file)
    return JSONResponse(content={"message": "PDF processing started"}, status_code=202)
