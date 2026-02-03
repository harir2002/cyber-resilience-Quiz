import smtplib
import socket
import sys

def check_connection(server, port, timeout=10):
    print(f"Testing connection to {server}:{port}...", end=" ", flush=True)
    try:
        if port == 465:
            s = smtplib.SMTP_SSL(server, port, timeout=timeout)
        else:
            s = smtplib.SMTP(server, port, timeout=timeout)
            s.starttls()
        
        print("✅ SUCCESS!")
        print(f"   Response: {s.ehlo()}")
        s.quit()
        return True
    except socket.timeout:
        print("❌ TIMEOUT (Firewall blocking?)")
    except ConnectionRefusedError:
        print("❌ CONNECTION REFUSED")
    except OSError as e:
        print(f"❌ NETWORK ERROR: {e}")
    except Exception as e:
        print(f"❌ FAILED: {type(e).__name__} - {e}")
    return False

print("--- SMTP CONNECTIVITY DIAGNOSTIC ---")
print("Checking access to Gmail from this machine...")
print("-" * 40)

# Check standard TLS port
t1 = check_connection("smtp.gmail.com", 587)

# Check SSL port
t2 = check_connection("smtp.gmail.com", 465)

print("-" * 40)
if not t1 and not t2:
    print("CONCLUSION: Your network is blocking ALL access to Gmail SMTP.")
    print("Solution: Try a mobile hotspot or different network.")
elif t1:
    print("CONCLUSION: Port 587 is OPEN. Please configure .env with SMTP_PORT=587")
elif t2:
    print("CONCLUSION: Port 465 is OPEN. Please configure .env with SMTP_PORT=465")
