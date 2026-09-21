# Lecture 12 — Worksheet (GA-12) & Exit Ticket

Name: ________________  Date: ______

## Part A — Header reading (from projected capture) (8 min)
1. IHL = 5 → header bytes: ________ 2. Total Length 365, IHL 5 → L4 payload bytes
   (TCP header 20): ________
3. TTL 61 observed. If initial TTL was 64, hops so far: ________
4. Protocol field 6 → ________; field 1 → ________

## Part B — ARP walk (pairs, 12 min)
Trace excerpt: frames 1–4 = ARP request (broadcast), ARP reply (unicast), ICMP echo,
ICMP echo reply. Hosts: A=192.168.10.23 (3c:7a:8f:15:22:9c), GW=192.168.10.1
(bc:24:11:2a:9f:01).
5. Frame 1 sender/target protocol addresses: ________ → ________
6. Frame 1 destination MAC: ________ Why that value? ________
7. Frame 2 is unicast to ________ and teaches A the mapping ________.
8. Now A wants 8.8.8.8. Whose MAC goes into the Ethernet header? ________
9. If 8.8.8.8's "MAC" never appears in any cache, what resolved it instead? ________

## Part C — Security (5 min)
10. Attacker broadcasts: "192.168.10.1 is-at de:ad:be:ef:00:01". Victim caches now map
    ________ to ________. Symptom users see: ________
11. Name two defenses: ________

## Exit ticket (3 items)
1. Best-effort means (one line): ________
2. ARP is (link-local / end-to-end): ________
3. TTL's purpose: ________
