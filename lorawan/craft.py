import argparse
import binascii
import os
from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.primitives.ciphers import algorithms

def validate_hex(input_str, expected_length=None, field_name=""):
    """Valide une entrée hexadécimale et sa longueur"""
    try:
        data = binascii.unhexlify(input_str)
        if expected_length and len(data) != expected_length:
            raise ValueError(f"{field_name} doit faire exactement {expected_length} octets")
        return data
    except binascii.Error:
        raise ValueError(f"{field_name} n'est pas une valeur hexadécimale valide")

def calculate_mic(key, data):
    """Calcule le MIC avec AES-CMAC"""
    cmac = CMAC(algorithms.AES(key))
    cmac.update(data)
    return cmac.finalize()[:4]

def build_join_request():
    print("\n=== Construction Join Request ===")
    mhdr = input("MHDR (hex, défaut 00): ") or "00"
    join_eui = input("JoinEUI (hex, 8 octets): ")
    dev_eui = input("DevEUI (hex, 8 octets): ")
    dev_nonce = input("DevNonce (hex, 2 octets, vide=aléatoire): ") or os.urandom(2).hex()
    app_key = input("AppKey (hex, 16 octets): ")

    # Validation des entrées
    validate_hex(mhdr, 1, "MHDR")
    join_eui = validate_hex(join_eui, 8, "JoinEUI")
    dev_eui = validate_hex(dev_eui, 8, "DevEUI")
    dev_nonce = validate_hex(dev_nonce, 2, "DevNonce")
    app_key = validate_hex(app_key, 16, "AppKey")

    # Construction payload
    payload = bytes([int(mhdr, 16)]) + join_eui + dev_eui + dev_nonce

    # Calcul MIC
    mic = calculate_mic(app_key, payload)

    return payload + mic

def build_join_accept():
    print("\n=== Construction Join Accept ===")
    mhdr = input("MHDR (hex, défaut 20): ") or "20"
    join_nonce = input("JoinNonce (hex, 3 octets): ")
    net_id = input("NetID (hex, 3 octets): ")
    dev_addr = input("DevAddr (hex, 4 octets): ")
    dl_settings = input("DLSettings (hex, défaut 00): ") or "00"
    rx_delay = input("RXDelay (hex, défaut 01): ") or "01"
    cflist = input("CFList (hex, 16 octets, vide=optionnel): ") or ""
    app_key = input("AppKey (hex, 16 octets): ")

    # Validation des entrées
    validate_hex(mhdr, 1, "MHDR")
    join_nonce = validate_hex(join_nonce, 3, "JoinNonce")
    net_id = validate_hex(net_id, 3, "NetID")
    dev_addr = validate_hex(dev_addr, 4, "DevAddr")
    validate_hex(dl_settings, 1, "DLSettings")
    validate_hex(rx_delay, 1, "RXDelay")
    if cflist:
        cflist = validate_hex(cflist, 16, "CFList")
    app_key = validate_hex(app_key, 16, "AppKey")

    # Construction payload
    payload = bytes([int(mhdr, 16)]) + join_nonce + net_id + dev_addr
    payload += validate_hex(dl_settings, 1) + validate_hex(rx_delay, 1)
    if cflist:
        payload += cflist

    # Calcul MIC
    mic = calculate_mic(app_key, payload)

    return payload + mic

def build_data_frame():
    print("\n=== Construction Data Frame ===")
    mhdr = input("MHDR (hex, défaut 40 pour Unconfirmed Up): ") or "40"
    dev_addr = input("DevAddr (hex, 4 octets): ")
    f_ctrl = input("FCtrl (hex, défaut 00): ") or "00"
    f_cnt = input("FCnt (hex, 2 octets, défaut 0000): ") or "0000"
    f_opts = input("FOpts (hex, 0-15 octets): ") or ""
    payload = input("FRMPayload (hex): ") or ""
    nwk_key = input("NwkSKey (hex, 16 octets): ")

    # Validation des entrées
    validate_hex(mhdr, 1, "MHDR")
    dev_addr = validate_hex(dev_addr, 4, "DevAddr")
    validate_hex(f_ctrl, 1, "FCtrl")
    f_cnt = validate_hex(f_cnt, 2, "FCnt")
    if f_opts:
        f_opts = validate_hex(f_opts, None, "FOpts")
        if len(f_opts) > 15:
            raise ValueError("FOpts ne doit pas dépasser 15 octets")
    if payload:
        payload = validate_hex(payload, None, "FRMPayload")
    nwk_key = validate_hex(nwk_key, 16, "NwkSKey")

    # Construction payload
    phy_payload = bytes([int(mhdr, 16)]) + dev_addr
    phy_payload += validate_hex(f_ctrl, 1) + f_cnt
    if f_opts:
        phy_payload += f_opts
    if payload:
        phy_payload += payload

    # Calcul MIC (simplifié - à améliorer selon specs LoRaWAN)
    mic = calculate_mic(nwk_key, phy_payload)

    return phy_payload + mic

def main():
    parser = argparse.ArgumentParser(description="LoRaWAN Packet Crafter")
    parser.add_argument('type', choices=['join_request', 'join_accept', 'data'], help="Type de trame")
    args = parser.parse_args()

    try:
        if args.type == 'join_request':
            packet = build_join_request()
        elif args.type == 'join_accept':
            packet = build_join_accept()
        elif args.type == 'data':
            packet = build_data_frame()

        print("\n=== Trame finale ===")
        print("Hex: ", binascii.hexlify(packet).decode('utf-8').upper())
        print("Taille:", len(packet), "octets")
    except ValueError as e:
        print(f"\nErreur: {e}")

if __name__ == "__main__":
    main()
