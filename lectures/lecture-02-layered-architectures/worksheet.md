# Lecture 02 — Worksheet (GA-02) & Exit Ticket

Name: ________________  Date: ______

## Part A — Annotated frame dissection (pairs, 12 min)

An Ethernet frame from a provided capture excerpt (hex shown on the board/handout):

```
Destination: bc:24:11:2a:9f:01   Source: 3c:7a:8f:15:22:9c
EtherType: 0x0800
IPv4: Version 4, IHL 5, Total Length 1040, Protocol 6,
      Src 192.168.10.23, Dst 142.250.183.68
TCP: Src Port 49152, Dst Port 443, Flags [ACK], Seq ..., Len 1000
Payload: 1000 bytes (encrypted)
```

1. Which module reads EtherType? What does 0x0800 tell it? ________
2. Which module reads Protocol=6? What does it deliver to? ________
3. What identifies the *process* that receives this data? ________
4. Name the PDU at each level as this frame was *built* downward:
   message → ________ → ________ → ________
5. Which two headers were added *last* and *first* respectively? ________

## Part B — Overhead math (5 min)
6. App message 1,200 B; TCP adds 20 B; IP adds 20 B; Ethernet adds 18 B. Compute total
   overhead percentage.

## Part C — Standards matching (5 min)
7. Match: `802.11` · `RFC 9293` · `802.1Q` · `root zone` · `802.3` →
   body: IETF / IEEE / ICANN

## Part D — Reasoning (5 min)
8. Give one concrete network feature that is *harder* to build because of layering, and say
   which information gets lost across layers. (Hint: what does a Wi-Fi AP not know about
   your TCP flow?)

## Exit ticket (3 items, individual)
1. The 5 layers of our model, top to bottom, with the PDU name for each: ________
2. The header field that chooses between TCP and UDP on arrival: ________
3. The body that standardizes Ethernet: ________
