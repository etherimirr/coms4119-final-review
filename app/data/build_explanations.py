#!/usr/bin/env python3
"""Build skeleton explanations.json with one entry per slide.

Extracts the title (first non-empty line) of each page via pdftotext -f N -l N.
Merges in hand-written detailed entries from explanations_detail.json if present.
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # /Users/jyj/Desktop/4119
PDFS = [
    # pre-mid
    "lec1-intro","lec2-basics1","lec3-basics2","lec4-basics3",
    "lec5-web","lec6-video","lec7","lec8-dns","lec9-p2p",
    "lec10-transport","lec11-reliability","lec12-tcp","lec13-congestion",
    "midterm-preview",
    # post-mid
    "lec14","lec16","lec17","lec18","lec19","lec20","lec21","lec22","lec23",
    "final-preview",
]
OUT = ROOT / "app" / "data" / "explanations.json"
DETAIL = ROOT / "app" / "data" / "explanations_detail.json"

def pdf_pages(name):
    pdf = ROOT / f"{name}.pdf"
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", info)
    return int(m.group(1))

def first_line(name, page):
    # extract just this page
    txt = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(ROOT / f"{name}.pdf"), "-"],
        capture_output=True, text=True
    ).stdout
    for line in txt.splitlines():
        s = line.strip()
        # filter obvious page numbers, footers
        if not s: continue
        if re.fullmatch(r"\d{1,3}", s): continue
        if re.fullmatch(r"[\d\-: ]+", s): continue
        if re.match(r"^(Transport|Network|Application|Link) Layer:?\s*\d", s, re.I): continue
        return s
    return "(无标题)"

def topic_guess(name):
    return {
        "lec14": ["TCP 拥塞控制","AIMD","slow start","CUBIC","BBR","ECN"],
        "lec16": ["TCP 公平性","Network 数据面","forwarding","router","LPM","switching fabric","IP datagram","subnet","CIDR","DHCP","NAT"],
        "lec17": ["期中","IP","DHCP","subnet"],
        "lec18": ["IPv6","tunneling","control plane","link state","Dijkstra","distance vector","Bellman-Ford","count to infinity"],
        "lec19": ["intra-AS","OSPF","inter-AS","BGP","policy","hot potato"],
        "lec20": ["SDN","OpenFlow","match+action","data link layer","error detection","parity","checksum","CRC"],
        "lec21": ["MAC","ALOHA","CSMA/CD","Ethernet","frame","MAC address","ARP","DHCP"],
        "lec22": ["switch","self learning","VLAN","router vs switch","wireless physical","pathloss"],
        "lec23": ["radio propagation","SNR","multipath","fading","wireless MAC","hidden terminal","RTS/CTS","CSMA/CA","backoff","802.11"],
        "final-preview": ["recap","example questions","TCP/IP/BGP/wireless 综合"],
        "lec1-intro":        ["intro","internet","layering","ISP","what is the Internet"],
        "lec2-basics1":      ["protocol","packet vs circuit","performance","delays","throughput"],
        "lec3-basics2":      ["layering","encapsulation","headers"],
        "lec4-basics3":      ["RTT","BDP","performance metrics"],
        "lec5-web":          ["HTTP","persistent","non-persistent","RTT counting","cookie","web cache","conditional GET"],
        "lec6-video":        ["video","DASH","streaming","CDN"],
        "lec7":              ["socket","UDP socket","TCP socket","welcome socket"],
        "lec8-dns":          ["DNS","hierarchy","recursive","iterative","RR","root","TLD","authoritative"],
        "lec9-p2p":          ["P2P","BitTorrent","file distribution time","tit-for-tat","DHT"],
        "lec10-transport":   ["transport","UDP","TCP intro","multiplexing","demultiplexing","port"],
        "lec11-reliability": ["RDT","Stop-and-Wait","GBN","Selective Repeat","sequence number","ACK","checksum","sliding window"],
        "lec12-tcp":          ["TCP","3WHS","seq/ACK","flow control","rwnd","timeout","fast retransmit","close"],
        "lec13-congestion":  ["congestion control","slow start","AIMD","ssthresh","fairness","intro"],
        "midterm-preview":   ["midterm review","example questions"],
    }.get(name, [])

def main():
    detail = {}
    if DETAIL.exists():
        detail = json.loads(DETAIL.read_text())

    out = {}
    topic_for = {f: topic_guess(f) for f in PDFS}
    for f in PDFS:
        n = pdf_pages(f)
        arr = []
        for p in range(1, n+1):
            entry = {
                "title": first_line(f, p),
                "topics": [],
            }
            # carry over topic tags only on first page
            if p == 1:
                entry["topics"] = topic_for[f]
            # merge detailed override
            key = f"{f}:{p}"
            if key in detail:
                entry.update(detail[key])
            arr.append(entry)
        out[f] = arr
        print(f"{f}: {n} pages → built")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
