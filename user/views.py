from django.shortcuts import render
from user.models import Identity
from django.views import generic
from django.http import HttpResponse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'user/wallet.html'
    context_object_name = 'identity'

    def get_queryset(self):
        return Identity.objects.all()


def KeyView(request):
    private_key = gen_key()
    encode_public_key(private_key)
    encode_private_key(private_key)
    return HttpResponse(generate_identity_sign(private_key))

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
        identit.signature = signature
        identit.save()
