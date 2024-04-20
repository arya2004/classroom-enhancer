from multiprocessing import context
import re
from django.http import HttpResponse
from django.shortcuts import render
from .forms import MintForm

#nft
from thirdweb import ThirdwebSDK
from thirdweb.types.nft import NFTMetadataInput
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3
import os

load_dotenv()

PRIVATE_KEY = "e5851304dea001993487e60cf4181685d38d52e87bc80075a0aa691f3da5521e"

RPC_URL = "https://polygon-rpc.com"

provider = Web3(Web3.HTTPProvider(RPC_URL))

signer = Account.from_key(PRIVATE_KEY)

sdk = ThirdwebSDK(provider, signer)
NFT_COLLECTION_ADDRESS = "0x99d9Ffd18c1f0bF31D400E98d7d5D5046A2A16dA" #You can create one from thirdweb.com
nft_collection = sdk.get_nft_collection(NFT_COLLECTION_ADDRESS)

def home(request):
    context = {}
    return render(request,'home.html',context)

def issue_certificate(request):
    form = MintForm()
    context = {'form':form}
    if request.method == 'POST':
        name = request.POST.get("student_name")
        cgpa = request.POST.get("student_cgpa")
        wallet = request.POST.get("student_wallet")
        url = request.POST.get("certificate_url")

        # nft_collection.mint_to(wallet,NFTMetadataInput.from_json({ 
        #     "name": "BE", 
        #     "description": "Certificate issued by ABC University", 
        #     "image": url,
        #     "properties": {'student_name':name, 'cgpa':cgpa}
        # }))
        return render(request,'success.html',context)
    return render(request,'issue_certificate.html',context)

def verify_certificate(request):
    context = {}
    return render(request,'verify_certificate.html',context)

def apply_masters(request):
    context = {}
    return render(request,'apply_masters.html',context)

def view_certificates(request):
    nfts = request.GET.get('nfts')
    context = {'nfts':nfts}
    return render(request,'view_certificates.html',context)