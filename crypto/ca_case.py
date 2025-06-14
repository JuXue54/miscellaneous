import base64
import binascii
from inspect import signature

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from cryptography import x509
from cryptography.hazmat.primitives import serialization

from crypto.crypto_util import RSAUtil


def calculate_der_hash(pem_cert):
    """
    提取公钥
    """
    pem_lines = pem_cert.strip().splitlines()
    base64_str = "".join(line.strip() for line in pem_lines[1:-1])
    der_data = base64.b64decode(base64_str)

    # 解析证书并提取 TBSCertificate（ASN.1 结构）
    cert = x509.load_der_x509_certificate(der_data)
    cert_der = cert.public_bytes(encoding=serialization.Encoding.DER)
    # return SHA256.new(cert_der).hexdigest()
    # return base64.b64encode(cert_der).decode()
    return cert_der


def calculate_tbs_hash(pem_cert):
    """
    提取证书中的正文和签名
    """
    # 提取 PEM 中的 Base64 部分
    pem_lines = pem_cert.strip().splitlines()
    base64_str = "".join(line.strip() for line in pem_lines[1:-1])
    der_data = base64.b64decode(base64_str)

    # 解析证书并提取 TBSCertificate（ASN.1 结构）
    cert = x509.load_der_x509_certificate(der_data)
    tbs_data = cert.tbs_certificate_bytes  # 直接获取 TBSCertificate 的 DER 编码

    # 计算哈希（示例用 SHA-256）
    return tbs_data, cert.signature

def extract_tbs_and_signature(pem_cert: str) -> tuple:
    """
    提取证书中的正文和签名
    @see calculate_tbs_hash
    """
    """从PEM证书中提取TBSCertificate和签名"""
    # 去掉PEM头尾并解码Base64
    pem_data = pem_cert.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "")
    der_data = base64.b64decode(pem_data)

    # 解析DER格式的证书（ASN.1序列）
    cert_asn1 = DerSequence()
    cert_asn1.decode(der_data)

    # TBSCertificate是证书的第一个元素
    tbs_certificate = cert_asn1[0]

    # 签名是第二个元素
    # 取后面的256位
    signature = cert_asn1[2][-256:]  # 注意：签名是BIT STRING，可能需要去掉填充字节
    return tbs_certificate, signature


def verify_all(*ca):
    """
    验证整个证书链
    """
    pem_certs = []
    for x in ca:
        with open(x, 'r') as f:
            pem_certs.append(f.read())

    for i in range(1, len(pem_certs)):
        pub_key = calculate_der_hash(pem_certs[i-1])
        message, signature = extract_tbs_and_signature(pem_certs[i])
        rsa_util = RSAUtil()
        rsa_util.load_public_key(pub_key)

        res = rsa_util.verify_sign(message, base64.b64encode(signature))
        if not res:
            return False
    return True

def test():
    # ca的公钥
    model = """
    BE 17 E8 EC BE 29 0A CB FE B9 2D 61 31 FD 33 24
    08 32 2E 59 E8 21 D4 D8 30 BE 6E 10 C8 84 A0 3F
    BA 14 E5 DE FD 7A 8C 92 1B 7B CE 84 2D F0 FF 78
    C4 32 E8 A9 A0 7D 5F 06 DA 7B 9B 4B 53 A6 C6 1B
    02 17 21 E1 70 3B AD FB 83 EB 08 54 81 A8 DE 12
    B2 D5 C6 88 96 30 F9 02 FC 39 D4 BD B8 22 EF 80
    49 99 D0 62 B8 61 D0 49 DE CB C2 CB 97 A5 31 06
    1B D7 D8 5D C6 D3 54 DE 52 01 36 2A 0D F6 DE C5
    B6 31 4C CC 15 25 6A 15 6F A9 6B 04 48 0C DE 00
    41 AA 28 80 8B 2F 34 D3 1B B5 36 AD 3B 25 D0 88
    42 40 6C 36 91 6D 65 B2 19 86 C0 D2 7F 39 46 58
    FE 30 12 60 50 DC EE BB 73 E6 57 90 5A F6 0D CA
    D7 04 4B 47 6A 6F 34 1A 9D 92 36 1A 2E D9 4E 54
    ED 47 AC 0C BF F1 80 B2 BA FF 47 7B E9 39 C4 54
    C4 94 54 99 19 F1 57 99 AF E2 14 22 5B E8 2E BB
    63 2D BA AE 81 BD 13 DC E6 17 5B E0 90 53 49 01
    """.replace('\n','').replace('\t', '').replace(' ','')
    n = int(model, 16)
    e = int("010001",16)
    pub_key = RSA.construct((n,e))
    rsa_util = RSAUtil()
    rsa_util.load_public_key(pub_key)

    # 获取deepseek的证书和签名
    with open('_.deepseek.com', 'r') as file:
        content = file.read()
    message, signature = calculate_tbs_hash(content)

    success = rsa_util.verify_sign(message, base64.b64encode(signature))
    if success:
        print('Certificate verified successfully')
    else:
        print('Certificate verification failed')





def main():
    success = verify_all('DigiCert Global Root G2.crt','GeoTrust TLS RSA CA G1.crt', '_.deepseek.com')
    if success:
        print('Certificate verified successfully')
    else:
        print('Certificate verification failed')



if __name__ == '__main__':
    main()
