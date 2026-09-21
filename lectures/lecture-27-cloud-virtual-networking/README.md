# Lecture 27 — Cloud & Virtual Networking

| Field | Value |
|---|---|
| Module | 7 — Operations, Monitoring & Cloud |
| Depends on | L09 (VLANs), L13–L16 (addressing/routing), L25 (security policy) |
| CLOs addressed | **CLO6** (primary), CLO3 (cloud addressing), CLO7 (cloud security controls) |
| Bloom level | C3–C4 |
| Assessment artifact | Exit ticket; GA-27 mini-VPC submission |
| Lab | GA-27: build a mini-VPC in the VM lab (subnets, NAT, security rules) |
| Readings | PD §3.4, §4.3 (selected); instructor cloud notes (this package) |
| Prerequisites | L09, L13–L16, L25 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- How does a virtual switch differ from a physical one — and how do containers
  get their networks?
- What is a VPC, and how do its subnets/route tables/security groups map to the
  concepts you already own?
- How do load balancers differ at L4 vs L7?

## What you should be able to do afterwards
- Explain bridges, vNICs, overlays, and container networking (veth/pairs/NAT).
- Map VPC constructs (subnets, route tables, SGs vs ACLs) onto campus concepts.
- Build a mini-VPC: two subnets, NAT gateway, security rules — and verify flows.
- Choose L4 vs L7 balancing for a given service with justification.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-27. Read PD §3.5 (SDN section).
