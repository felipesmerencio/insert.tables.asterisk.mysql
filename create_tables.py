import os
from dotenv import load_dotenv
import pymysql

# depedencies: pip install python-dotenv pymysql

# Carregar variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Configurações de conexão com o banco de dados
host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = "asterisk"

# Definição das tabelas
tables = [
    """CREATE DATABASE IF NOT EXISTS `asterisk`;""",
    """CREATE TABLE IF NOT EXISTS asterisk.ps_aors (
        id VARCHAR(40) NOT NULL,
        contact VARCHAR(255) DEFAULT NULL,
        default_expiration INT DEFAULT NULL,
        mailboxes VARCHAR(80) DEFAULT NULL,
        max_contacts INT DEFAULT NULL,
        minimum_expiration INT DEFAULT NULL,
        remove_existing ENUM('yes','no') DEFAULT NULL,
        qualify_frequency INT DEFAULT NULL,
        authenticate_qualify ENUM('yes','no') DEFAULT NULL,
        maximum_expiration INT DEFAULT NULL,
        outbound_proxy VARCHAR(40) DEFAULT NULL,
        support_path ENUM('yes','no') DEFAULT NULL,
        qualify_timeout FLOAT DEFAULT NULL,
        voicemail_extension VARCHAR(40) DEFAULT NULL,
        UNIQUE KEY id (id),
        KEY ps_aors_id (id),
        KEY ps_aors_qualifyfreq_contact (qualify_frequency,contact)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""",
    """CREATE TABLE IF NOT EXISTS asterisk.`ps_auths` (
        id varchar(40) NOT NULL,
        auth_type enum('md5','userpass') DEFAULT NULL,
        nonce_lifetime int(11) DEFAULT NULL,
        md5_cred varchar(40) DEFAULT NULL,
        password varchar(80) DEFAULT NULL,
        realm varchar(40) DEFAULT NULL,
        username varchar(40) DEFAULT NULL,
        UNIQUE KEY id (id),
        KEY ps_auths_id (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """CREATE TABLE IF NOT EXISTS asterisk.`ps_contacts` (
        `id` varchar(255) DEFAULT NULL,
        `uri` varchar(255) DEFAULT NULL,
        `expiration_time` bigint(20) DEFAULT NULL,
        `qualify_frequency` int(11) DEFAULT NULL,
        `outbound_proxy` varchar(40) DEFAULT NULL,
        `path` text,
        `user_agent` varchar(255) DEFAULT NULL,
        `qualify_timeout` float DEFAULT NULL,
        `reg_server` varchar(20) DEFAULT NULL,
        `authenticate_qualify` enum('yes','no') DEFAULT NULL,
        `via_addr` varchar(40) DEFAULT NULL,
        `via_port` int(11) DEFAULT NULL,
        `call_id` varchar(255) DEFAULT NULL,
        `endpoint` varchar(40) DEFAULT NULL,
        `prune_on_boot` enum('yes','no') DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        UNIQUE KEY `ps_contacts_uq` (`id`,`reg_server`),
        KEY `ps_contacts_id` (`id`),
        KEY `ps_contacts_qualifyfreq_exp` (`qualify_frequency`,`expiration_time`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_domain_aliases` (
        `id` varchar(40) NOT NULL,
        `domain` varchar(80) DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_domain_aliases_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_endpoint_id_ips` (
        `id` varchar(40) NOT NULL,
        `endpoint` varchar(40) DEFAULT NULL,
        `match` varchar(80) DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_endpoint_id_ips_id` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_endpoints` (
        `id` varchar(40) NOT NULL,
        `transport` varchar(40) DEFAULT NULL,
        `aors` varchar(200) DEFAULT NULL,
        `auth` varchar(40) DEFAULT NULL,
        `context` varchar(40) DEFAULT NULL,
        `disallow` varchar(200) DEFAULT NULL,
        `allow` varchar(200) DEFAULT NULL,
        `direct_media` enum('yes','no') DEFAULT NULL,
        `connected_line_method` enum('invite','reinvite','update') DEFAULT NULL,
        `direct_media_method` enum('invite','reinvite','update') DEFAULT NULL,
        `direct_media_glare_mitigation` enum('none','outgoing','incoming') DEFAULT NULL,
        `disable_direct_media_on_nat` enum('yes','no') DEFAULT NULL,
        `dtmf_mode` enum('rfc4733','inband','info','auto') DEFAULT NULL,
        `external_media_address` varchar(40) DEFAULT NULL,
        `force_rport` enum('yes','no') DEFAULT NULL,
        `ice_support` enum('yes','no') DEFAULT NULL,
        `identify_by` enum('username','auth_username') DEFAULT NULL,
        `mailboxes` varchar(40) DEFAULT NULL,
        `moh_suggest` varchar(40) DEFAULT NULL,
        `outbound_auth` varchar(40) DEFAULT NULL,
        `outbound_proxy` varchar(40) DEFAULT NULL,
        `rewrite_contact` enum('yes','no') DEFAULT NULL,
        `rtp_ipv6` enum('yes','no') DEFAULT NULL,
        `rtp_symmetric` enum('yes','no') DEFAULT NULL,
        `send_diversion` enum('yes','no') DEFAULT NULL,
        `send_pai` enum('yes','no') DEFAULT NULL,
        `send_rpid` enum('yes','no') DEFAULT NULL,
        `timers_min_se` int(11) DEFAULT NULL,
        `timers` enum('forced','no','required','yes') DEFAULT NULL,
        `timers_sess_expires` int(11) DEFAULT NULL,
        `callerid` varchar(40) DEFAULT NULL,
        `callerid_privacy` enum('allowed_not_screened','allowed_passed_screened','allowed_failed_screened','allowed','prohib_not_screened','prohib_passed_screened','prohib_failed_screened','prohib','unavailable') DEFAULT NULL,
        `callerid_tag` varchar(40) DEFAULT NULL,
        `100rel` enum('no','required','yes') DEFAULT NULL,
        `aggregate_mwi` enum('yes','no') DEFAULT NULL,
        `trust_id_inbound` enum('yes','no') DEFAULT NULL,
        `trust_id_outbound` enum('yes','no') DEFAULT NULL,
        `use_ptime` enum('yes','no') DEFAULT NULL,
        `use_avpf` enum('yes','no') DEFAULT NULL,
        `media_encryption` enum('no','sdes','dtls') DEFAULT NULL,
        `inband_progress` enum('yes','no') DEFAULT NULL,
        `call_group` varchar(40) DEFAULT NULL,
        `pickup_group` varchar(40) DEFAULT NULL,
        `named_call_group` varchar(40) DEFAULT NULL,
        `named_pickup_group` varchar(40) DEFAULT NULL,
        `device_state_busy_at` int(11) DEFAULT NULL,
        `fax_detect` enum('yes','no') DEFAULT NULL,
        `t38_udptl` enum('yes','no') DEFAULT NULL,
        `t38_udptl_ec` enum('none','fec','redundancy') DEFAULT NULL,
        `t38_udptl_maxdatagram` int(11) DEFAULT NULL,
        `t38_udptl_nat` enum('yes','no') DEFAULT NULL,
        `t38_udptl_ipv6` enum('yes','no') DEFAULT NULL,
        `tone_zone` varchar(40) DEFAULT NULL,
        `language` varchar(40) DEFAULT NULL,
        `one_touch_recording` enum('yes','no') DEFAULT NULL,
        `record_on_feature` varchar(40) DEFAULT NULL,
        `record_off_feature` varchar(40) DEFAULT NULL,
        `rtp_engine` varchar(40) DEFAULT NULL,
        `allow_transfer` enum('yes','no') DEFAULT NULL,
        `allow_subscribe` enum('yes','no') DEFAULT NULL,
        `sdp_owner` varchar(40) DEFAULT NULL,
        `sdp_session` varchar(40) DEFAULT NULL,
        `tos_audio` varchar(10) DEFAULT NULL,
        `tos_video` varchar(10) DEFAULT NULL,
        `sub_min_expiry` int(11) DEFAULT NULL,
        `from_domain` varchar(40) DEFAULT NULL,
        `from_user` varchar(40) DEFAULT NULL,
        `mwi_from_user` varchar(40) DEFAULT NULL,
        `dtls_verify` varchar(40) DEFAULT NULL,
        `dtls_rekey` varchar(40) DEFAULT NULL,
        `dtls_cert_file` varchar(200) DEFAULT NULL,
        `dtls_private_key` varchar(200) DEFAULT NULL,
        `dtls_cipher` varchar(200) DEFAULT NULL,
        `dtls_ca_file` varchar(200) DEFAULT NULL,
        `dtls_ca_path` varchar(200) DEFAULT NULL,
        `dtls_setup` enum('active','passive','actpass') DEFAULT NULL,
        `srtp_tag_32` enum('yes','no') DEFAULT NULL,
        `media_address` varchar(40) DEFAULT NULL,
        `redirect_method` enum('user','uri_core','uri_pjsip') DEFAULT NULL,
        `set_var` text,
        `cos_audio` int(11) DEFAULT NULL,
        `cos_video` int(11) DEFAULT NULL,
        `message_context` varchar(40) DEFAULT NULL,
        `force_avp` enum('yes','no') DEFAULT NULL,
        `media_use_received_transport` enum('yes','no') DEFAULT NULL,
        `accountcode` varchar(80) DEFAULT NULL,
        `user_eq_phone` enum('yes','no') DEFAULT NULL,
        `moh_passthrough` enum('yes','no') DEFAULT NULL,
        `media_encryption_optimistic` enum('yes','no') DEFAULT NULL,
        `rpid_immediate` enum('yes','no') DEFAULT NULL,
        `g726_non_standard` enum('yes','no') DEFAULT NULL,
        `rtp_keepalive` int(11) DEFAULT NULL,
        `rtp_timeout` int(11) DEFAULT NULL,
        `rtp_timeout_hold` int(11) DEFAULT NULL,
        `bind_rtp_to_media_address` enum('yes','no') DEFAULT NULL,
        `voicemail_extension` varchar(40) DEFAULT NULL,
        `mwi_subscribe_replaces_unsolicited` int(11) DEFAULT NULL,
        `deny` varchar(95) DEFAULT NULL,
        `permit` varchar(95) DEFAULT NULL,
        `acl` varchar(40) DEFAULT NULL,
        `contact_deny` varchar(95) DEFAULT NULL,
        `contact_permit` varchar(95) DEFAULT NULL,
        `contact_acl` varchar(40) DEFAULT NULL,
        `subscribe_context` varchar(40) DEFAULT NULL,
        `fax_detect_timeout` int(11) DEFAULT NULL,
        `contact_user` varchar(80) DEFAULT NULL,
        `asymmetric_rtp_codec` enum('yes','no') DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_endpoints_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_globals` (
        `id` varchar(40) NOT NULL,
        `max_forwards` int(11) DEFAULT NULL,
        `user_agent` varchar(255) DEFAULT NULL,
        `default_outbound_endpoint` varchar(40) DEFAULT NULL,
        `debug` varchar(40) DEFAULT NULL,
        `endpoint_identifier_order` varchar(40) DEFAULT NULL,
        `max_initial_qualify_time` int(11) DEFAULT NULL,
        `default_from_user` varchar(80) DEFAULT NULL,
        `keep_alive_interval` int(11) DEFAULT NULL,
        `regcontext` varchar(80) DEFAULT NULL,
        `contact_expiration_check_interval` int(11) DEFAULT NULL,
        `default_voicemail_extension` varchar(40) DEFAULT NULL,
        `disable_multi_domain` enum('yes','no') DEFAULT NULL,
        `unidentified_request_count` int(11) DEFAULT NULL,
        `unidentified_request_period` int(11) DEFAULT NULL,
        `unidentified_request_prune_interval` int(11) DEFAULT NULL,
        `default_realm` varchar(40) DEFAULT NULL,
        `mwi_tps_queue_high` int(11) DEFAULT NULL,
        `mwi_tps_queue_low` int(11) DEFAULT NULL,
        `mwi_disable_initial_unsolicited` enum('yes','no') DEFAULT NULL,
        `ignore_uri_user_options` enum('yes','no') DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_globals_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_registrations` (
        `id` varchar(40) NOT NULL,
        `auth_rejection_permanent` enum('yes','no') DEFAULT NULL,
        `client_uri` varchar(255) DEFAULT NULL,
        `contact_user` varchar(40) DEFAULT NULL,
        `expiration` int(11) DEFAULT NULL,
        `max_retries` int(11) DEFAULT NULL,
        `outbound_auth` varchar(40) DEFAULT NULL,
        `outbound_proxy` varchar(40) DEFAULT NULL,
        `retry_interval` int(11) DEFAULT NULL,
        `forbidden_retry_interval` int(11) DEFAULT NULL,
        `server_uri` varchar(255) DEFAULT NULL,
        `transport` varchar(40) DEFAULT NULL,
        `support_path` enum('yes','no') DEFAULT NULL,
        `fatal_retry_interval` int(11) DEFAULT NULL,
        `line` enum('yes','no') DEFAULT NULL,
        `endpoint` varchar(40) DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_registrations_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_registrations` (
    `id` varchar(40) NOT NULL,
    `auth_rejection_permanent` enum('yes','no') DEFAULT NULL,
    `client_uri` varchar(255) DEFAULT NULL,
    `contact_user` varchar(40) DEFAULT NULL,
    `expiration` int(11) DEFAULT NULL,
    `max_retries` int(11) DEFAULT NULL,
    `outbound_auth` varchar(40) DEFAULT NULL,
    `outbound_proxy` varchar(40) DEFAULT NULL,
    `retry_interval` int(11) DEFAULT NULL,
    `forbidden_retry_interval` int(11) DEFAULT NULL,
    `server_uri` varchar(255) DEFAULT NULL,
    `transport` varchar(40) DEFAULT NULL,
    `support_path` enum('yes','no') DEFAULT NULL,
    `fatal_retry_interval` int(11) DEFAULT NULL,
    `line` enum('yes','no') DEFAULT NULL,
    `endpoint` varchar(40) DEFAULT NULL,
    UNIQUE KEY `id` (`id`),
    KEY `ps_registrations_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_subscription_persistence` (
        `id` varchar(40) NOT NULL,
        `packet` varchar(2048) DEFAULT NULL,
        `src_name` varchar(128) DEFAULT NULL,
        `src_port` int(11) DEFAULT NULL,
        `transport_key` varchar(64) DEFAULT NULL,
        `local_name` varchar(128) DEFAULT NULL,
        `local_port` int(11) DEFAULT NULL,
        `cseq` int(11) DEFAULT NULL,
        `tag` varchar(128) DEFAULT NULL,
        `endpoint` varchar(40) DEFAULT NULL,
        `expires` int(11) DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_subscription_persistence_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_systems` (
        `id` varchar(40) NOT NULL,
        `timer_t1` int(11) DEFAULT NULL,
        `timer_b` int(11) DEFAULT NULL,
        `compact_headers` enum('yes','no') DEFAULT NULL,
        `threadpool_initial_size` int(11) DEFAULT NULL,
        `threadpool_auto_increment` int(11) DEFAULT NULL,
        `threadpool_idle_timeout` int(11) DEFAULT NULL,
        `threadpool_max_size` int(11) DEFAULT NULL,
        `disable_tcp_switch` enum('yes','no') DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_systems_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`ps_transports` (
        `id` varchar(40) NOT NULL,
        `async_operations` int(11) DEFAULT NULL,
        `bind` varchar(40) DEFAULT NULL,
        `ca_list_file` varchar(200) DEFAULT NULL,
        `cert_file` varchar(200) DEFAULT NULL,
        `cipher` varchar(200) DEFAULT NULL,
        `domain` varchar(40) DEFAULT NULL,
        `external_media_address` varchar(40) DEFAULT NULL,
        `external_signaling_address` varchar(40) DEFAULT NULL,
        `external_signaling_port` int(11) DEFAULT NULL,
        `method` enum('default','unspecified','tlsv1','sslv2','sslv3','sslv23') DEFAULT NULL,
        `local_net` varchar(40) DEFAULT NULL,
        `password` varchar(40) DEFAULT NULL,
        `priv_key_file` varchar(200) DEFAULT NULL,
        `protocol` enum('udp','tcp','tls','ws','wss') DEFAULT NULL,
        `require_client_cert` enum('yes','no') DEFAULT NULL,
        `verify_client` enum('yes','no') DEFAULT NULL,
        `verify_server` enum('yes','no') DEFAULT NULL,
        `tos` varchar(10) DEFAULT NULL,
        `cos` int(11) DEFAULT NULL,
        `allow_reload` enum('yes','no') DEFAULT NULL,
        UNIQUE KEY `id` (`id`),
        KEY `ps_transports_id` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """,
    """
    CREATE DATABASE IF NOT EXISTS `asteriskcdrdb`;""",
    """
    CREATE TABLE IF NOT EXISTS asteriskcdrdb.`cdr` (
        `calldate` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
        `clid` varchar(80) NOT NULL DEFAULT '',
        `src` varchar(80) NOT NULL DEFAULT '',
        `dst` varchar(80) NOT NULL DEFAULT '',
        `dcontext` varchar(80) NOT NULL DEFAULT '',
        `channel` varchar(80) NOT NULL DEFAULT '',
        `dstchannel` varchar(80) NOT NULL DEFAULT '',
        `lastapp` varchar(80) NOT NULL DEFAULT '',
        `lastdata` varchar(80) NOT NULL DEFAULT '',
        `duration` int(11) NOT NULL DEFAULT 0,
        `billsec` int(11) NOT NULL DEFAULT 0,
        `disposition` varchar(45) NOT NULL DEFAULT '',
        `amaflags` int(11) NOT NULL DEFAULT 0,
        `accountcode` varchar(20) NOT NULL DEFAULT '',
        `uniqueid` varchar(32) NOT NULL DEFAULT '',
        `userfield` varchar(255) NOT NULL DEFAULT '',
        `recordingfile` varchar(255) NOT NULL DEFAULT '',
        `cnum` varchar(40) NOT NULL DEFAULT '',
        `cnam` varchar(40) NOT NULL DEFAULT '',
        `outbound_cnum` varchar(40) NOT NULL DEFAULT '',
        `outbound_cnam` varchar(40) NOT NULL DEFAULT '',
        `dst_cnam` varchar(40) NOT NULL DEFAULT '',
        `did` varchar(50) NOT NULL DEFAULT '',
        KEY `IDX_UNIQUEID` (`uniqueid`),
        KEY `idx_cdr_dst` (`dst`)
    ) ENGINE=InnoDB;
    """,
    """
    CREATE TABLE IF NOT EXISTS asteriskcdrdb.`cel` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `eventtype` varchar(30) NOT NULL,
        `eventtime` datetime NOT NULL,
        `cid_name` varchar(80) NOT NULL,
        `cid_num` varchar(80) NOT NULL,
        `cid_ani` varchar(80) NOT NULL,
        `cid_rdnis` varchar(80) NOT NULL,
        `cid_dnid` varchar(80) NOT NULL,
        `exten` varchar(80) NOT NULL,
        `context` varchar(80) NOT NULL,
        `channame` varchar(80) NOT NULL,
        `appname` varchar(80) NOT NULL,
        `appdata` varchar(80) NOT NULL,
        `amaflags` int(11) NOT NULL,
        `accountcode` varchar(20) NOT NULL,
        `uniqueid` varchar(32) NOT NULL,
        `linkedid` varchar(32) NOT NULL,
        `peer` varchar(80) NOT NULL,
        `userdeftype` varchar(255) NOT NULL,
        `eventextra` varchar(255) DEFAULT NULL,
        `userfield` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        KEY `uniqueid_index` (`uniqueid`),
        KEY `linkedid_index` (`linkedid`)
    ) ENGINE=InnoDB;
    """,
    """
    CREATE TABLE IF NOT EXISTS asterisk.`check` (
        `id` varchar(40) NOT NULL
    ) ENGINE=InnoDB;
    """,
]


def create_tables(connection):
    """Cria as tabelas no banco de dados"""
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(table)
        connection.commit()


def main():
    # Conectar ao banco de dados
    connection = pymysql.connect(
        host=host, port=port, user=username, password=password, database=database
    )

    try:
        create_tables(connection)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
