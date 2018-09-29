from django.shortcuts import render
from user.models import Identity
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from user.serializers import IdentitySerializer
from rest_framework import generics
import json
import hashlib

# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'user/wallet.html'
    context_object_name = 'identity'

    def get_queryset(self):
        return Identity.objects.all()


class SerializerView(LoginRequiredMixin, generics.ListCreateAPIView):
    model = Identity
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()

    def post(self, request):
        name = request.data['name']
        signature = request.data['signature']
        for iden in Identity.objects.all():
            if iden.name == name and iden.signature == signature:
                return HttpResponse("<h1>Access Granted &#128076</h1>")
            else:
                return HttpResponse("<h1>The problem you face when you are given too much control &#128532</h1>")
        
def KeyView(request):
    try:
        f = open('private_key.pem', 'rb+')
        return HttpResponse('<h1>Keys are already generated.&#128273;</h1>')
    except FileNotFoundError:
        private_key = gen_key()
        encode_public_key(private_key)
        encode_private_key(private_key)
        generate_identity_sign(private_key)
        return HttpResponse('Private and Public Keys have been created!')
        

def gen_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    return private_key

def encode_private_key(pk):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_key.pem', 'wb+') as f:
        f.write(pem)

def encode_public_key(pk):
    public_key = pk.public_key()
    pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb+') as f:
        f.write(pem)

def generate_identity_sign(pk):
    identity = Identity.objects.all()
    signature_list = []
    for identit in identity:
        signature = pk.sign(
            (identit.name+identit.aadhar_number).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
        ),
            hashes.SHA256()
        )
        identit.signature = hashlib.sha256(signature).hexdigest()
        identit.save()
