# Lecture 27 — Instructor Teaching Notes
## Cloud & Virtual Networking (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO6 primary; CLO3/CLO7 supporting |
| Textbook anchor | PD §3.4, §4.3 (selected) |

---

## 1. Objectives hook
Board: **"You already know VLANs, subnets, route tables, and firewall policy. A VPC
is those four ideas with new names and an API. Let's translate."**

Hook (2 min): `ip link` on the podium VM showing bridges, veths, and a container
namespace — "the cloud is *this*, replicated by an API instead of hands."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L25 policy recall; the virtual `ip link` |
| 6–26 | Concept 1 | Virtual primitives: bridges, vNICs, veth, namespaces, overlays |
| 26–46 | Concept 2 | VPC model: subnets, route tables, SGs vs ACLs, NAT gateways |
| 46–58 | Concept 3 | Load balancing L4 vs L7; hybrid connectivity (concept) |
| 58–63 | Break | — |
| 63–75 | GA-27 briefing | Mini-VPC topology in the VM lab |
| 75–108 | GA-27 (build) | Pairs build + verify the mini-VPC |
| 108–116 | Findings | One pair traces a flow through their build |
| 116–120 | Summary + exit ticket | — |

## 3. Concept walkthrough

### 3.1 Virtual primitives (20 min)
- **Bridge (virtual switch):** `br0`-style L2 device inside the kernel — L08's
  switch algorithm, software edition (students watched its FDB learn in L08's
  demo; now it's a building block).
- **veth pairs:** virtual patch cables — one end in a namespace, other in the
  bridge; the universal plumbing under containers.
- **Network namespaces:** isolated stacks (interfaces, routes, firewall) — the
  cloud's tenancy primitive in miniature; containers = namespaces + cgroups
  (one sentence each).
- **Container networking patterns (named, with one-liners):** bridge (default:
  veth + NAT), host, macvlan, overlay (multi-host encapsulation — the VXLAN
  idea, L09's trunking grown up).
- **Overlay concept:** tunnels between hosts make a virtual L2 across the data
  center — the cloud's "VLAN that spans regions" (concept level; VXLAN named).

### 3.2 The VPC model (20 min)
- **VPC = your private address space in a provider's fabric.** Translation table
  (board, students copy):
  | Campus concept | VPC construct |
  |---|---|
  | VLAN | Subnet (a CIDR in the VPC) |
  | Router (L3) | Route tables (attached per subnet) |
  | Firewall policy | Security groups (instance-level, stateful) |
  | ACLs | Network ACLs (subnet-level, stateless) |
  | NAT device | NAT gateway (outbound-only) |
  | Load balancer | LB service (L4 or L7) |
- **SG vs NACL (the exam-grade distinction):** SG = instance-level, stateful,
  allow-only; NACL = subnet-level, stateless, allow+deny, ordered. Students
  predict which catches what.
- **Public/private subnet pattern:** IGW for public; NAT gateway for private
  outbound — L14's NAT discipline reappears as managed service.
- **Hybrid (concept, 3 min):** VPN/interconnect attach on-prem to VPC — CS-04's
  branch↔cloud story gets its vocabulary.

### 3.3 Load balancing & scaling (12 min)
- **L4 (transport) balancing:** 5-tuple hashing/flows; fast, protocol-agnostic;
  can't see paths beyond connections.
- **L7 balancing:** TLS termination, path/host routing, header cookies —
  smarter, costlier; health checks decide backend membership (L29's monitoring
  vocabulary previews).
- **Scaling shapes:** round-robin vs least-connections (queueing intuition from
  L01!); sticky sessions (state vs stateless backends).

### Reference diagram — Overlay vs underlay

```text
VM-A 10.0.1.5 ═══ VXLAN tunnel ═══ VM-B 10.0.1.9  (tenant overlay)
         outer IPs: 172.16.0.11 ←──→ 172.16.0.12  (underlay fabric)
```

## 4. Important definitions
Bridge · vNIC · veth pair · Network namespace · Container network patterns ·
Overlay/VXLAN (concept) · VPC · Subnet (public/private) · Route table ·
Security group vs Network ACL · Internet vs NAT gateway · L4 vs L7 LB ·
Health check · Hybrid connectivity (named).

## 5. Real-world examples
- **`docker inspect`'s network section** is the translation table made JSON —
  show it live; SGs/NACLs map to nftables rules students wrote in L25.
- **"Why is my VM unreachable?"** in cloud = overwhelmingly route table or SG
  misconfiguration — the two-sided check from L16 applies *per subnet*.

## 6. Mathematical/technical example
Mini-VPC CIDR design (GA-27's planning step): VPC 10.30.0.0/16 → public
10.30.1.0/24, private 10.30.2.0/24 (L13's VLSM discipline in cloud clothes);
route tables: public→IGW; private→NAT; SG pairs allowing 443 from anywhere to
public-web, private-app allowed only *from* public-web's SG — SG-to-SG references
(the pattern students must discover in the lab).

## 7. GA-27: mini-VPC build (33 min, after briefing)
VM-lab topology (namespaces/bridges per handout): "VPC router" VM with 3 nets;
two "subnets" (separate bridges), one public instance (serves 443 via a tiny
server), one private instance (outbound-only via NAT rule); SG-equivalent
nftables rules per the translation table; verification flow: public reach works;
private outbound works; private inbound fails (the *proof* of the pattern).
⚠ Verify image tooling (bridges/namespaces/nftables); handout carries exact
commands; CS-04 teams may reuse this build as their cloud stage.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "The cloud is a different kind of networking" | Same L2/L3 concepts, API-controlled (the translation table IS the lecture) |
| "Security groups are stateful ACLs" | Different objects: SG instance/stateful/allow-only; NACL subnet/stateless/ordered |
| "Containers have their own TCP/IP stack hardware" | Namespaces + veth + bridge — all software |
| "NAT gateway = security" | Outbound-only convenience; SGs/NACLs are the policy (L25's line, again) |
| "L7 LB is always better" | Cost/latency/complexity; L4 for raw protocol throughput — CLO6 evaluation |

## 9. Suggested practical demonstration
The hook's `ip link` expanded: create a namespace, attach a veth, ping across it —
"the cloud tenancy primitive in 60 seconds". ⚠ Pre-script; keep the GA-27
reference build as backup.

## 10. Classroom activities
- **Translation-table relay:** teams race to map 8 campus constructs → VPC names.
- **SG/NACL triage:** 4 flow scenarios (reply blocked by NACL but not SG...);
  classify which object drops it — the stateful/stateless discriminator drilled.

## 11. Problem-solving questions
1. Private subnet instance needs OS updates. Which construct enables it, and why
   not an IGW?
2. Your NACL allows inbound 443 but the reply fails. Why? (stateless — egress
   ephemeral must be allowed)
3. SG-to-SG reference: write the pair of rules for public-web → private-app:5432.
4. Why does L4 LB health checking differ from L7's? (connection vs HTTP probe)
5. Overlay networks carry L2 across hosts: what does that *change* about MTU?
   (encapsulation overhead — L15/L25's recurring tax)

## 12. Formative assessment (with answers)
- MCQ: A VPC subnet is closest to a campus → **VLAN**.
- MCQ: Stateful, instance-level, allow-only describes → **security groups**.
- MCQ: Outbound-only internet access for private subnets uses → **a NAT gateway**.
- Short: one reason to choose L4 over L7 balancing. → throughput/protocol-
  agnostic simplicity (or: no TLS termination cost).

## 13. Exit ticket
1. SG vs NACL: ________ (two differences)
2. Public/private subnet pattern: public uses ________; private uses ________.
3. L4 sees ________; L7 additionally sees ________.

## 14. Anticipated difficulties
- Provider-specific vocabulary varies (AWS/GCP/Azure names differ); the lecture
  teaches *concepts* and names the big-three terms once — vendor-neutral rule
  honored explicitly.
- GA-27's namespace choreography is the term's fiddliest lab: the handout's
  copy-paste blocks + a verification checklist keep pairs on track.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify GA-27 build end-to-end on the image; reference build ready
- [ ] Print handouts + translation-table cards; SG/NACL triage scenarios
- [ ] Board pre-write: translation table; SG/NACL table; public/private diagram
- [ ] Coordinate with CS-04 teams reusing the build

## 16. Timing fallbacks
Hybrid connectivity to reading; GA-27's verification flow (the pattern proof) is
protected; the L4/L7 segment can compress to the triage activity only.

## 17. References
- PD §3.4, §4.3 (selected); provider VPC documentation (AWS/GCP/Azure — cite the
  one used in the lab ⚠); Docker networking docs (named patterns).
- LAB-13 handout (nftables continuity); GA-27 handout.
- ⚠ VERIFY image tooling and provider docs currency this semester.
