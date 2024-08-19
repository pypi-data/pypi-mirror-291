#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Author: AnhNT
    Company: MobioVN
    Date created: 26/02/2021

"""

from .config import (
    SystemConfigKeys, UrlConfig, KafkaTopic, CodeErrorDecrypt, CodeErrorEncrypt, RedisKeyCache,
    lru_redis_cache
)
import datetime
import requests
from dateutil.parser import parse
import base64
from .mobio_admin_sdk import MobioAdminSDK
from .aes_cipher import CryptUtil
from mobio.libs.ciphers import MobioCrypt2, MobioCrypt4
import json
from flask import request
from .aes_cipher import AESCipher
from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager
import os
from .date_utils import ConvertTime
import copy
from jose import jwt
from mobio.libs.caching import LRUCacheDict
from mobio.libs.Singleton import Singleton
import time


def decrypt_data(enc_data):
    try:
        while len(enc_data) % 4 != 0:
            enc_data = enc_data + "="
        decrypt_resp = AESCipher().decrypt(enc_data)
        if decrypt_resp:
            return json.loads(decrypt_resp)
        return None
    except Exception as e:
        print("admin_sdk::decrypt_data: Exception: %s" % e)
        return None


def get_merchant_auth(merchant_id):
    result = get_merchant_config_host(merchant_id)
    if not result or not result.get("jwt_algorithm") or not result.get("jwt_secret_key"):
        print("admin_sdk::get_merchant_auth: jwt_algorithm None, jwt_secret_key None")
        raise ValueError("admin_sdk::can not get merchant config auth ")
    return {
        SystemConfigKeys.JWT_ALGORITHM: result.get("jwt_algorithm"),
        SystemConfigKeys.JWT_SECRET_KEY: result.get("jwt_secret_key"),
    }


@lru_redis_cache.add()
def get_info_merchant_config(
        merchant_id,
        key=None,
        token_value=None,
        admin_version=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.ADMIN_CONFIG).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": SystemConfigKeys.MOBIO_TOKEN}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    data = result.get("data", {})
    if key:
        return data.get(key)
    return data


def check_basic_auth(partner_key):
    try:
        partner_info = get_partner_info_decrypt(partner_key, decrypt=True)
        if not partner_info and partner_info.get("data"):
            return False
        # partner_info = decrypt_data(partner_info_enc)
        expire_time = parse(partner_info.get("expired_time"))
        if expire_time.replace(tzinfo=datetime.timezone.utc) < ConvertTime.get_utc_now():
            print("admin_sdk::check_basic_auth: reach expire time: %s" % str(expire_time))
            return False
        return True
    except Exception as e:
        print("admin_sdk::check_basic_auth: error: %s" % e)
        return False


def get_partner_info_decrypt(partner_key, decrypt=False):
    partner_info_enc = get_partner_info_by_key(partner_key)
    if not decrypt:
        return partner_info_enc
    else:
        if not partner_info_enc or not isinstance(partner_info_enc, dict) or not partner_info_enc.get("data"):
            return partner_info_enc
        partner_info_dec = MobioCrypt2.d1(partner_info_enc.get("data"), enc="utf-8")
        return {"code": 200, "data": json.loads(partner_info_dec)}


@lru_redis_cache.add()
def get_partner_info_by_key(partner_key):
    if not partner_key:
        return None
    adm_url = str(UrlConfig.PARTNER_INFO_CIPHER_ENCRYPT).format(
        host=MobioAdminSDK().admin_host,
        version=MobioAdminSDK().admin_version,
        partner_id=partner_key,
    )
    resp = requests.get(
        adm_url,
        headers=MobioAdminSDK().request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    return resp.json()


def check_basic_auth_v2(partner_key):
    try:
        partner_info_enc = get_partner_info_by_key_v2(partner_key)
        if not partner_info_enc:
            return False
        # partner_info_dec = MobioCrypt2.d1(partner_info_enc, enc="utf-8")
        # partner_info = json.loads(partner_info_dec)
        partner_info = decrypt_data(partner_info_enc)
        expire_time = parse(partner_info.get("expired_time"))
        if expire_time.replace(tzinfo=datetime.timezone.utc) < ConvertTime.get_utc_now():
            print("admin_sdk::check_basic_auth: reach expire time: %s" % str(expire_time))
            return False
        return True
    except Exception as e:
        print("admin_sdk::check_basic_auth: error: %s" % e)
        return False


@lru_redis_cache.add()
def get_partner_info_by_key_v2(partner_key):
    if not partner_key:
        return None
    adm_url = str(UrlConfig.PARTNER_INFO).format(
        host=MobioAdminSDK().admin_host,
        version=MobioAdminSDK().admin_version,
        partner_id=partner_key,
    )
    resp = requests.get(
        adm_url,
        headers=MobioAdminSDK().request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    resp.raise_for_status()
    status_code = resp.status_code
    if status_code == 200:
        result = resp.json()
        enc_data = result["data"]
        return enc_data
    else:
        print("admin_sdk::get_expire_time_by_key: error: status_code = %d" % status_code)
        return None


class Base64(object):
    @staticmethod
    def encode(data):
        try:
            byte_string = data.encode("utf-8")
            encoded_data = base64.b64encode(byte_string)
            return encoded_data.decode(encoding="UTF-8")
        except Exception as ex:
            print(ex)
            return ""

    @staticmethod
    def decode(encoded_data):
        try:
            if isinstance(encoded_data, bytes):
                encoded_data = encoded_data.decode("UTF-8")
            decoded_data = base64.urlsafe_b64decode(
                encoded_data + "=" * (-len(encoded_data) % 4)
            )
            return decoded_data.decode(encoding="UTF-8")
        except Exception as ex:
            print(ex)
            return encoded_data


@lru_redis_cache.add()
def get_info_merchant_brand_sub_brand(
        merchant_id,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.MERCHANT_RELATED).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}

    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_info_staff(
        merchant_id,
        account_id,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.STAFF_INFO).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
        account_id=account_id,
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_list_info_staff(
        merchant_id,
        params=None,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.LIST_STAFF_INFO).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_list_parent_merchant(
        merchant_id,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.MERCHANT_PARENT).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_list_profile_group(
        merchant_id=None,
        params=None,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.LIST_PROFILE_GROUP).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if merchant_id:
        request_header["X-Merchant-Id"] = merchant_id
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_list_subbrands(
        params=None,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.LIST_SUBBRANDS_BY_MERCHANT).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


@lru_redis_cache.add()
def get_info_subbrand(
        subbrand_id=None,
        admin_version=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.GET_INFO_SUBBRAND).format(
        host=MobioAdminSDK().admin_host, version=api_version, subbrand_id=subbrand_id
    )
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}

    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    return result


def push_kafka_log_action_account(json_mess):
    if not json_mess:
        raise ValueError("data none")
    if not json_mess.get("account_id"):
        raise ValueError("account_id not found")
    if not json_mess.get("merchant_id"):
        raise ValueError("merchant_id not found")
    if not json_mess.get("created_time"):
        raise ValueError("created_time not found")
    if not json_mess.get("action_name_vi") and not json_mess.get("action_name_en"):
        raise ValueError("action_name_vi and action_name_en not found")
    if not json_mess.get("action_name_vi") and json_mess.get("action_name_en"):
        json_mess["action_name_vi"] = json_mess.get("action_name_en")
    if json_mess.get("action_name_vi") and not json_mess.get("action_name_en"):
        json_mess["action_name_en"] = json_mess.get("action_name_vi")
    json_mess["source"] = "admin_sdk"
    push_message_kafka(
        topic=KafkaTopic.LogActionAccount, data={"message": json_mess}
    )


def push_message_kafka(topic: str, data: dict, key=None):
    key = key if key else topic
    KafkaProducerManager().flush_message(topic=topic, key=key, value=data)


@lru_redis_cache.add()
def get_merchant_config_host(
        merchant_id,
        key_host=None,
        admin_version=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    if SystemConfigKeys.vm_type and not CryptUtil().license_server_valid():
        raise ValueError("license server invalid")

    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.GET_DETAIL_MERCHANT_CONFIG).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    request_header = {}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    param = {"fields": ",".join(["internal_host", "module_host", "public_host", "config_host"])}
    response = requests.get(
        adm_url,
        params=param,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    data = result.get("data", {}) if result and result.get("data", {}) else {}
    if key_host:
        return data.get(key_host)
    return data


@lru_redis_cache.add()
def get_merchant_config_other(
        merchant_id,
        list_key=None,
        admin_version=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    if admin_version and admin_version in MobioAdminSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.GET_DETAIL_MERCHANT_CONFIG).format(
        host=MobioAdminSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    request_header = {}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    param = None
    if list_key and isinstance(list_key, list):
        param = {"fields": ",".join(list_key)}
    response = requests.get(
        adm_url,
        params=param,
        headers=request_header,
        timeout=request_timeout,
    )
    # response.raise_for_status()
    result = response.json()
    data = result.get("data", {}) if result and result.get("data", {}) else {}
    return data


@lru_redis_cache.add()
def get_all_key_uri_from_merchant(
        merchant_id=None,
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    adm_url = str(UrlConfig.GET_SERVER_FROM_MERCHANT).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    params = {
        "merchant_id": merchant_id,
    }
    # if key_uri_module:
    #     params["key_module"] = key_uri_module
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    if result and result.get("data"):
        return result.get("data")
    else:
        return None


@lru_redis_cache.add()
def get_list_all_server_uri(
        token_value=None,
        request_timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioAdminSDK().admin_version
    adm_url = str(UrlConfig.GET_LIST_SERVER_FROM_MODULE).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    params = {
    }
    if token_value:
        request_header = {"Authorization": token_value}
    else:
        request_header = {"Authorization": request.headers.get("Authorization")}
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    if result and result.get("data"):
        return result.get("data")
    else:
        return None


def get_server_uri_from_merchant(merchant_id, key_module):
    server_id, db_uri = "", ""
    try:
        if SystemConfigKeys.vm_type:
            result = get_all_key_uri_from_merchant(
                merchant_id=merchant_id,
                token_value=SystemConfigKeys.MOBIO_TOKEN,
            )
            if result:
                server_id = result.get("server_id")
                db_uri = result.get(key_module)
    except Exception as er:
        err_msg = "admin_sdk::get_server_uri_from_merchant ERR: {}".format(er)
        print(err_msg)
    if not server_id or not db_uri:
        server_id = key_module
        db_uri = os.environ.get(key_module)
    return server_id, db_uri


def get_server_uri_default_from_module(key_module):
    server_id = key_module
    db_uri = os.environ.get(key_module)
    return server_id, db_uri


@lru_redis_cache.add()
def get_list_api_register_app(merchant_id, app_id):
    result = get_merchant_config_host(merchant_id)
    if not result or not result.get("data-out-app-api-service-host"):
        return None
    api_url = "{host}/datasync/api/v1.0/api-out/app/api-register".format(
        host=result.get("data-out-app-api-service-host")
    )
    params = {
        "app_id": app_id
    }
    request_header = {
        "Authorization": SystemConfigKeys.MOBIO_TOKEN,
        "X-Merchant-Id": merchant_id
    }
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        api_url,
        params=params,
        headers=request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    result = response.json()
    if result and result.get("data"):
        return result.get("data")
    else:
        return None


@lru_redis_cache.add()
def get_list_fields_config_encrypt(merchant_id, module):
    api_version = MobioAdminSDK().admin_version
    adm_url = str(UrlConfig.GET_LIST_FIELD_CONFIG_ENCRYPT).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    params = {"module": module}
    request_header = {
        "Authorization": SystemConfigKeys.MOBIO_TOKEN,
        "X-Merchant-Id": merchant_id
    }
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    result = response.json()
    if result and result.get("data"):
        return result.get("data")
    else:
        return []


@lru_redis_cache.add()
def get_detail_kms_config(kms_id):
    api_version = MobioAdminSDK().admin_version
    adm_url = str(UrlConfig.GET_DETAIL_KMS_CONFIG).format(
        host=MobioAdminSDK().admin_host, version=api_version
    )
    params = {"kms_id": kms_id}
    request_header = {
        "Authorization": SystemConfigKeys.MOBIO_TOKEN,
    }
    if MobioAdminSDK().request_header:
        request_header.update(MobioAdminSDK().request_header)
    response = requests.get(
        adm_url,
        params=params,
        headers=request_header,
        timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    result = response.json()
    if result and result.get("data"):
        return result.get("data")
    else:
        return {}


def get_info_field_config(merchant_id, module, field):
    field_config = {}
    try:
        fields_config = get_list_fields_config_encrypt(merchant_id, module)
        if fields_config:
            for item in fields_config:
                if item.get("field") == field and item.get("kms_id") and item.get("enc_level") != "enc_frontend":
                    field_config["kms_id"] = item.get("kms_id")
                    field_config["kms_info"] = item.get("kms_info")
                    # field_config["normalize_config"] = item.get("normalize_config", "")
                    break
    except Exception as e:
        print("admin_sdk::get_kms_id_from_fields_config: error: {}".format(e))
    return field_config


def build_response_from_list(list_value):
    data = {}
    for item in list_value:
        data[item] = item
    return {"code": 200, "data": data}


def encrypt_field_by_config(merchant_id, module, field, values):
    field_config = get_info_field_config(merchant_id, module, field)
    kms_id, kms_info = None, None
    if field_config and isinstance(field_config, dict):
        kms_id = field_config.get("kms_id")
        kms_info = field_config.get("kms_info")
    if isinstance(values, str):
        values = [values]
    if kms_id and kms_info:
        kms_type = kms_info.get("kms_type", "kms_mobio")
        if kms_type == "kms_mobio":
            data_response = process_kms_mobio_encrypt(values)
        elif kms_type == "kms_viettel":
            data_response = process_kms_viettel_encrypt(kms_info, values)
        else:
            data_response = build_response_from_list(values)
    else:
        data_response = build_response_from_list(values)
    return data_response


def process_kms_mobio_encrypt(values):
    data = {}
    data_error = {}
    for item in values:
        if not item:
            continue
        try:
            item_format = MobioCrypt4.e1(item)
        except:
            item_format = None
        if item_format:
            data[item] = item_format
        else:
            data_error[item] = CodeErrorEncrypt.encrypt_error
    return {"data": data, "data_error": data_error}


def decrypt_field_by_config(merchant_id, module, field, values):
    field_config = get_info_field_config(merchant_id, module, field)
    kms_id, kms_info = None, None
    if field_config and isinstance(field_config, dict):
        kms_id = field_config.get("kms_id")
        kms_info = field_config.get("kms_info")
    if isinstance(values, str):
        values = [values]
    if kms_id and kms_info:
        kms_type = kms_info.get("kms_type", "kms_mobio")
        if kms_type == "kms_mobio":
            data_response = process_kms_mobio_decrypt(values)
        elif kms_type == "kms_viettel":
            data_response = process_kms_viettel_decrypt(kms_info, values)
        else:
            data_response = build_response_from_list(values)
    else:
        data_response = build_response_from_list(values)
    return data_response


def process_kms_mobio_decrypt(values):
    data = {}
    data_error = {}
    for item in values:
        if not item:
            continue
        try:
            item_format = MobioCrypt4.d1(item, enc='UTF-8')
        except:
            item_format = None
        if item_format:
            data[item] = item_format
        else:
            data_error[item] = CodeErrorDecrypt.decrypt_error
    return {"data": data, "data_error": data_error}


def kms_viettel_get_token(kms_id):
    try:
        key_cache = RedisKeyCache.kms_viettel_get_token.format(kms_id)
        token_key = MobioAdminSDK().redis_get_value(key_cache)
        if token_key:
            return token_key.decode('utf-8')
        else:
            api_version = MobioAdminSDK().admin_version
            adm_url = str(UrlConfig.GET_TOKEN_KMS_CONFIG).format(
                host=MobioAdminSDK().admin_host, version=api_version
            )
            params = {"kms_id": kms_id}
            request_header = {
                "Authorization": SystemConfigKeys.MOBIO_TOKEN,
            }
            if MobioAdminSDK().request_header:
                request_header.update(MobioAdminSDK().request_header)
            response = requests.get(
                adm_url,
                params=params,
                headers=request_header,
                timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            result = response.json()
            if result and result.get("data"):
                token_key = result.get("data").get("access_token")
                expires_in = int(result.get("data").get("expires_in"))
                expires_in = expires_in - 30 if expires_in > 30 else expires_in
                MobioAdminSDK().redis_set_value_expire(key_cache, token_key, time_seconds=expires_in)
                return token_key
    except Exception as er:
        print("admin_sdk::kms_viettel_get_token: error: {}".format(er))
    return None


def build_data_error_by_code(list_data, error_code):
    data_error = {}
    for item in list_data:
        data_error[item] = error_code
    return data_error


def request_kms_viettel_encrypt(kms_info, access_token, list_data):
    data_result = {
        "data": {}, "data_error": {}
    }
    try:
        kms_enc = kms_info.get("kms_enc")
        api_url = kms_enc.get("api_url")
        request_header = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json"
        }
        body_request = {
            "msisdns": list_data
        }
        response = requests.post(
            api_url,
            headers=request_header,
            json=body_request,
            timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        result = response.json()
        print("admin_sdk:: encrypt status: {}, text: {}".format(response.status_code, result))
        if result.get("content"):
            for item in result.get("content"):
                if item.get("value"):
                    data_result["data"][item.get("key")] = item.get("value")
                else:
                    data_result["data_error"][item.get("key")] = CodeErrorEncrypt.encrypt_api_error
            return data_result
        data_result["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
    except Exception as er:
        print("admin_sdk::request_kms_viettel_encrypt: error: {}".format(er))
        data_result["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_timeout)
    return data_result


def request_kms_viettel_decrypt(kms_info, access_token, list_data):
    data_result = {
        "data": {}, "data_error": {}
    }
    try:
        kms_dec = kms_info.get("kms_dec")
        api_url = kms_dec.get("api_url")
        request_header = {
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": "application/json"
        }
        body_request = {
            "msisdns": list_data
        }
        response = requests.post(
            api_url,
            headers=request_header,
            json=body_request,
            timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        result = response.json()
        print("admin_sdk:: decrypt status: {}, text: {}".format(response.status_code, result))
        if result.get("content"):
            for item in result.get("content"):
                if item.get("value"):
                    data_result["data"][item.get("key")] = item.get("value")
                else:
                    data_result["data_error"][item.get("key")] = CodeErrorEncrypt.encrypt_api_error
            return data_result
        data_result["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
    except Exception as er:
        print("admin_sdk::request_kms_viettel_encrypt: error: {}".format(er))
        data_result["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_timeout)
    return data_result


def split_list(input_list, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(input_list), n):
        yield input_list[i: i + n]


def process_kms_viettel_encrypt(kms_info, list_data):
    data_response = {"data": {}, "data_error": {}}
    try:
        kms_id = kms_info.get("kms_id")
        access_token = kms_viettel_get_token(kms_id)
        if access_token:
            list_chunk = split_list(list_data, 50)
            for chunk in list_chunk:
                data_result = request_kms_viettel_encrypt(kms_info, access_token, chunk)
                data_response["data"].update(data_result.get("data", {}))
                data_response["data_error"].update(data_result.get("data_error", {}))
            return data_response
    except Exception as er:
        print("admin_sdk::process_kms_viettel_encrypt: error: {}".format(er))
    data_response["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
    return data_response


def process_kms_viettel_decrypt(kms_info, list_data):
    data_response = {"data": {}, "data_error": {}}
    try:
        kms_id = kms_info.get("kms_id")
        access_token = kms_viettel_get_token(kms_id)
        if access_token:
            list_chunk = split_list(list_data, 50)
            for chunk in list_chunk:
                data_result = request_kms_viettel_decrypt(kms_info, access_token, chunk)
                data_response["data"].update(data_result.get("data", {}))
                data_response["data_error"].update(data_result.get("data_error", {}))
            return data_response
    except Exception as er:
        print("admin_sdk::process_kms_viettel_decrypt: error: {}".format(er))
    data_response["data_error"] = build_data_error_by_code(list_data, CodeErrorEncrypt.encrypt_api_error)
    return data_response


def get_config_time_and_currency(merchant_id):
    data_config = {
        "config_time": {
            "timezone": 7,
            "text": "(UTC+07:00) Bangkok, Hanoi, Jakarta",
            "location": "Asia/Saigon",
        },
        "currency_code": "vnd",
        "lang_default": "vi",
    }
    data = get_config_merchant_for_fields(merchant_id)
    if data:
        if data.get("config_time"):
            data_config.update({"config_time": data.get("config_time")})
        if data.get("currency_code"):
            data_config.update({"currency_code": data.get("currency_code")})
        if data.get("lang_default"):
            data_config.update({"lang_default": data.get("lang_default")})
    return data_config


def get_config_merchant_for_fields(merchant_id):
    list_field = ["config_time", "currency_code", "lang_default"]
    return get_merchant_config_other(merchant_id, list_field)


def convert_datetime_to_format(merchant_id: str, from_date: datetime.datetime,
                               format_type=ConvertTime.FORMAT_ddmmYYYY, tz=None, lang=None):
    if format_type not in ConvertTime.all_format:
        raise ValueError("format type not defind")
    date_input = copy.deepcopy(from_date)
    if tz is not None:
        date_input = ConvertTime.add_timezone_to_date(date_input, tz)
    if lang is None:
        lang = 'vi'
        list_field = ["lang_default"]
        data = get_merchant_config_other(merchant_id, list_field)
        if data:
            if data.get("lang_default"):
                lang = data.get("lang_default")
    return ConvertTime.convert_date_to_format(time_in=date_input, convert_type=format_type, lang=lang)


@lru_redis_cache.add()
def get_config_jwt_anonymous(merchant_id):
    """
    :param merchant_id:
    :return:  {
            "algorithm": algorithm,
            "secret_key": secret_key,
            "exp": expire_time,
        }
    """
    try:
        api_version = MobioAdminSDK().admin_version
        adm_url = str(UrlConfig.GET_CONFIG_JWT_ANONYMOUS).format(
            host=MobioAdminSDK().admin_host, version=api_version
        )
        request_header = {
            "Authorization": SystemConfigKeys.MOBIO_TOKEN,
            "X-Merchant-Id": merchant_id
        }
        if MobioAdminSDK().request_header:
            request_header.update(MobioAdminSDK().request_header)
        response = requests.get(
            adm_url,
            headers=request_header,
            timeout=MobioAdminSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        if result and result.get("data"):
            return result.get("data")
        else:
            return {}
    except Exception as er:
        print("admin_sdk::get_config_jwt_anonymous: error: {}".format(er))
        return {}


@Singleton
class ConfigJWT:

    def __init__(self):
        self.config_anonymous = LRUCacheDict(expiration=3600)
        self.config_auth = LRUCacheDict(expiration=3600)
        self.config_basic = LRUCacheDict(expiration=900)

    def get_config_anonymous(self, merchant_id):
        data = None
        try:
            try:
                data = self.config_anonymous.getitem(merchant_id)
            except:
                data = None
            if not data:
                data = get_config_jwt_anonymous(merchant_id)
                if data:
                    self.config_anonymous.set_item(merchant_id, data)
        except Exception as er:
            print("admin_sdk::get_config_anonymous: error: {}".format(er))
        return data

    def get_config_auth(self, merchant_id):
        data = None
        try:
            try:
                data = self.config_auth.getitem(merchant_id)
            except:
                data = None
            if not data:
                data = get_merchant_auth(merchant_id)
                if data:
                    self.config_auth.set_item(merchant_id, data)
        except Exception as er:
            print("admin_sdk::get_config_auth: error: {}".format(er))
        return data

    def get_config_basic(self, basic_key):
        data = None
        try:
            try:
                data = self.config_basic.getitem(basic_key)
            except:
                data = None
            if not data:
                if check_basic_auth_v2(basic_key):
                    data = "allow"
                    self.config_basic.set_item(basic_key, data)
                else:
                    data = "deny"
                    self.config_basic.set_item(basic_key, data)
        except Exception as er:
            print("admin_sdk::get_config_auth: error: {}".format(er))
        return data


def create_jwt_anonymous(merchant_id, data_jwt, session_time):
    if not merchant_id or not isinstance(merchant_id, str):
        raise ValueError("merchant_id not none")
    if not data_jwt or not isinstance(data_jwt, dict):
        raise ValueError("data_jwt not none")
    # if not isinstance(data_jwt.get("permissions"), dict):
    #     raise ValueError("permissions not valid")
    jwt_config = ConfigJWT().get_config_anonymous(merchant_id)
    if not jwt_config:
        raise ValueError("jwt config not none")
    algorithm = jwt_config.get("algorithm")
    secret_key = jwt_config.get("secret_key")
    exp = jwt_config.get("exp")
    if isinstance(session_time, int) and session_time > 0:
        exp = session_time
    time_start = time.time()
    data_jwt.update({
        "jwt_type": "anonymous",
        "exp": time_start + exp,
        "iat": time_start,
        "merchant_id": merchant_id,
    })
    encoded = jwt.encode(data_jwt, secret_key, algorithm=algorithm)
    return encoded

