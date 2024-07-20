from django.views.generic import View
from django.urls import reverse
from .forms import PdfForm,MergeForm,RotateForm
from django.shortcuts import render,HttpResponse
from pypdf import PdfReader, PdfWriter
import json
from io import BytesIO
import uuid
from os.path import getsize

class PdfUtils():

    @staticmethod
    def compress_img(filename:str,pgq):
        '''this function is used to compress any pdf. it primarily focuses on images.
        it takes two arguments one is the file name and the other is the quality of the compressed file
        '''
        writer = PdfWriter(clone_from=filename)

        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=pgq)
        
        fname = 'static/'+filename.replace('uploads','download')
        with open(fname, "wb") as f:
            writer.write(f)
        

    @staticmethod
    def pdfmerger(listpdf:list):
        '''this is used to mrege pdf files it takes list of file names as agruments
        and merges all of them into a single file'''
        merger = PdfWriter()
        for file in listpdf:
            merger.append(file)
        
        merger.write('merger.pdf')
        merger.close()

    @staticmethod
    def rotatepdf(filename,angle):
        reader = PdfReader(filename)
        writer = PdfWriter()

        for index,pages in enumerate(reader.pages):
            writer.add_page(pages)
            writer.pages[index].rotate(angle=angle)

        with open(filename, "wb") as f:
            writer.write(f)

    @staticmethod
    def splitpdf(filename,begin,end,count=1):
        reader = PdfReader(filename)
        writer = PdfWriter()

        for page in reader.pages[begin-1:end]:
            writer.add_page(page)
        with open(f"{filename.replace('.pdf','')}-split-{count}.pdf", "wb") as f:
            writer.write(f)


    @staticmethod
    def multisplit(filename,tupple):
        count = 0
        for i in tupple:
            PdfUtils.splitpdf(filename=filename,begin=i[0],end=i[1],count=count)
            count += 1

    @staticmethod
    def selectivesplit(filename,listofpages):
        reader = PdfReader(filename)
        writer = PdfWriter()

        for i in listofpages:
            writer.add_page(reader.pages[i-1])
        with open(filename, "wb") as f:
            writer.write(f)


class Home(View):
    def get(self,request):
        return render(request,'website/home.html')


class Compress(View):

    def get(self,request,id=''):
        form = PdfForm()
        ctx = {
            'form':form,
            'url':reverse("compress"),
        }
        return render(request,'website/compress.html',context=ctx)
    
    def post(self,request):
        form = PdfForm(request.POST,request.FILES)
        unique = str(uuid.uuid4())
        if(form.is_valid()):
            data = request.FILES['file'].read()
            compat = BytesIO(data)
            reader = PdfReader(compat)
                        
            writer = PdfWriter(clone_from=reader)

            for page in writer.pages:
                for img in page.images:
                    img.replace(img.image, quality=20)

            writer.write(f'static/download/{unique}.pdf')
            fname = f'download/{unique}.pdf'
            fsize = getsize("static/"+fname)/(10**6)
            ctx = {
                'fname':fname,
                'sieze':fsize
            }

        return HttpResponse(json.dumps(ctx))


class Merge(View):
    def get(self,request):
        form = MergeForm()
        ctx = {
            'form':form,
            'url':reverse("merge"),
        }
        return render(request,'website/Merge.html',context=ctx)
    def post(self,request):
        form = MergeForm(request.POST,request.FILES)
        if(form.is_valid()):
            unique = str(uuid.uuid4())
            data = request.FILES.getlist('file')
            merger = PdfWriter()
            for i in data:
                compat = BytesIO(i.read())
                merger.append(compat)

            merger.write(f'static/download/{unique}.pdf')
            fname = f'download/{unique}.pdf'
            fsize = getsize("static/"+fname)/(10**6)
            ctx = {
                'fname':fname,
                'sieze':fsize
            }

        return HttpResponse(json.dumps(ctx))


class Rotate(View):
    def get(self,request):
        form = RotateForm()
        ctx = {
            'form':form,
            'url':reverse("rotate"),
        }
        return render(request,'website/Rotate.html',ctx)
    def post(self,request):
        form = RotateForm(request.POST,request.FILES)
        unique = str(uuid.uuid4())
        if(form.is_valid()):
            data = request.FILES['file'].read()
            reader = BytesIO(data)
            reader = PdfReader(reader)
            writer = PdfWriter()

            for index,pages in enumerate(reader.pages):
                writer.add_page(pages)
                writer.pages[index].rotate(angle=90)

            
            writer.write(f'static/download/{unique}.pdf')
            fname = f'download/{unique}.pdf'
            fsize = getsize("static/"+fname)/(10**6)
            ctx = {
                'fname':fname,
                'sieze':fsize
            }

        return HttpResponse(json.dumps(ctx))


class Download(View):
    def get(self,request,id):
        ctx = {
            'id':id
        }
        return render(request, 'download_page.html',context=ctx)