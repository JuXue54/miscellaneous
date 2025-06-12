import base64
from inspect import signature

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import DerSequence
from cryptography import x509
from cryptography.hazmat.primitives import serialization

from crypto.crypto_util import RSAUtil


def calculate_tbs_hash(pem_cert):
    # 提取 PEM 中的 Base64 部分
    pem_lines = pem_cert.strip().splitlines()
    base64_str = "".join(line.strip() for line in pem_lines[1:-1])
    der_data = base64.b64decode(base64_str)

    # 解析证书并提取 TBSCertificate（ASN.1 结构）
    cert = x509.load_der_x509_certificate(der_data)
    tbs_data = cert.tbs_certificate_bytes  # 直接获取 TBSCertificate 的 DER 编码

    # 计算哈希（示例用 SHA-256）
    # digest = hashes.Hash(hashes.SHA256())
    # digest.update(tbs_data)
    # return digest.finalize().hex()
    return SHA256.new(tbs_data), cert.signature

def calculate_der_hash(pem_cert):
    pem_lines = pem_cert.strip().splitlines()
    base64_str = "".join(line.strip() for line in pem_lines[1:-1])
    der_data = base64.b64decode(base64_str)

    # 解析证书并提取 TBSCertificate（ASN.1 结构）
    cert = x509.load_der_x509_certificate(der_data)
    cert_der = cert.public_bytes(encoding=serialization.Encoding.DER)
    return SHA256.new(cert_der).hexdigest()


def extract_tbs_and_signature(pem_cert: str) -> tuple:
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
    signature = cert_asn1[2]  # 注意：签名是BIT STRING，可能需要去掉填充字节

    return tbs_certificate, signature




def main():
    with open('_.deepseek.com', 'r') as file:
        str = file.read()

    # deepseek公钥
    model = """
    B9 4D 2F 9B 70 CC A9 35 1B 53 25 78 22 ED 08 0D
    01 CA 5C 25 AD D6 D0 D2 5B 94 A4 0F 9C 4F 05 5D
    11 9B D2 C6 71 2B 0C 07 79 23 EE EE 34 F9 72 D5
    20 59 23 7A 23 C0 30 BB BB E5 7F 17 9B 4B 74 33
    C2 D6 90 2D 64 70 FE 94 42 2C CD 86 1D 63 51 50
    55 F1 2F 9C 2B 3E 76 44 8A A5 F0 E5 3A 17 B8 F6
    2B EF DD C5 84 FB 2F B6 57 71 42 63 8E B5 6E CF
    93 FA 73 E8 AB 13 42 17 11 CE D4 73 9D 62 04 B1
    09 23 87 F6 92 E1 4F 40 E4 C8 3B BA 13 58 2F 99
    FD 85 B1 FD F4 DD FE 31 76 44 80 2D E5 7F D7 8D
    F4 E6 ED A5 F7 1D 07 86 E7 65 56 FF 04 F3 99 AC
    16 1A 28 FE F7 EE AF 4F F1 8C F6 D9 A1 78 27 81
    CB 5C 0E 4F BF 21 67 0D FD 40 90 57 25 42 72 B6
    F1 B6 DC 54 7B 54 52 3F 02 98 72 46 38 B8 74 50
    88 13 A7 F4 BA 4C DF E5 21 F3 B2 CA 9F EC C9 0F
    F6 FD B5 9E FF B1 45 BC 36 63 A2 BE 62 14 8F C5
    """.replace('\n','').replace('\t', '').replace(' ','')

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
    message, signature = extract_tbs_and_signature(str)
    print(message.hex())
    print(signature.hex())

    success = rsa_util.verify_sign(message, signature)


    print(success)





if __name__ == '__main__':
    main()
