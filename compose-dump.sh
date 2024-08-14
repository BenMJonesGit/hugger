docker compose up -d
docker wait summary-app-1
tcpdump -r tcpdump_output/output.pcap
docker compose down
tcpdump -r tcpdump_output/output.pcap