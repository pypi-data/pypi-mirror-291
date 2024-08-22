use pyo3::pyclass;
use smcrypto::{sm2, sm4};
use crate::error::SMXError;

#[pyclass]
pub struct Key {
    pub sk: String,
    pub pk: String,
}


pub struct SMX {}
impl SMX {
    pub fn sm2_gen_keypair() -> Key {
        let (sk, pk) = sm2::gen_keypair();
        Key { sk, pk }
    }

    pub fn sm2_sign(sk: String, data: String) -> String {
        let sign_ctx = sm2::Sign::new(&sk);
        let sign = sign_ctx.sign(data.as_ref());
        String::from_utf8(sign).unwrap()
    }


    pub fn sm2_verify(sign: String, pk: String, data: String) -> bool {
        let sign = sign.into_bytes();
        let verify_ctx = sm2::Verify::new(&pk);
        verify_ctx.verify(data.as_ref(), &sign)
    }

    pub fn sm2_encrypt(pk: String, data: String) -> String {
        let enc_ctx = sm2::Encrypt::new(&pk);
        String::from_utf8(enc_ctx.encrypt(data.as_ref())).unwrap()
    }
    pub fn sm2_decrypt(sk: String, data: String) -> String {
        let dec_ctx = sm2::Decrypt::new(&sk);
        String::from_utf8(dec_ctx.decrypt(&(data.as_ref()))).unwrap()
    }
    pub fn sm4_encrypt(mode: String, data: String, key: String, iv: String) -> Result<String, SMXError> {
        if mode == "ecb" {
            let sm4_ecb = sm4::CryptSM4ECB::new(key.as_ref());
            String::from_utf8(sm4_ecb.encrypt_ecb(data.as_ref())).map_err(|e| SMXError::EncryptionError(e.to_string()))
        } else if mode == "cbc" {
            let sm4_cbc = sm4::CryptSM4CBC::new(key.as_ref(), iv.as_ref());
            String::from_utf8(sm4_cbc.encrypt_cbc(data.as_ref())).map_err(|e| SMXError::EncryptionError(e.to_string()))
        } else {
            Err(SMXError::InvalidMode)
        }
    }

    pub fn sm4_decrypt(mode: String, data: String, key: String, iv: String) -> Result<String, SMXError> {
        if mode == "ecb" {
            let sm4_ecb = sm4::CryptSM4ECB::new(key.as_ref());
            let dec_ecb = sm4_ecb.decrypt_ecb(&(data.as_ref()));
            String::from_utf8(dec_ecb).map_err(|e| SMXError::DecryptionError(e.to_string()))
        } else if mode == "cbc" {
            let sm4_cbc = sm4::CryptSM4CBC::new(key.as_ref(), iv.as_ref());
            let dec_cbc = sm4_cbc.decrypt_cbc(&(data.as_ref()));
            String::from_utf8(dec_cbc).map_err(|e| SMXError::DecryptionError(e.to_string()))
        } else {
            Err(SMXError::InvalidMode)
        }
    }
}
