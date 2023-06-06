
from PyPDF2 import PdfReader
from concurrent import futures
import pdf2text_pb2
import pdf2text_pb2_grpc
import grpc
import io


class Pdf2TextServicer(pdf2text_pb2_grpc.Pdf2TextServicer):

    def Convert(self, request, context):
        reader = PdfReader(io.BytesIO(request.payload))
        number_of_pages = len(reader.pages)
        text = ""
        for page_num in range(number_of_pages):
            page = reader.pages[page_num]
            text += page.extract_text()

        return pdf2text_pb2.ConvertResponse(text=text)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pdf2text_pb2_grpc.add_Pdf2TextServicer_to_server(
        Pdf2TextServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


print("pdf2text service is up and running")

serve()
