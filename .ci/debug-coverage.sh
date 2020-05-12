#!/usr/bin/env bash

# SOURCE: https://coverage.readthedocs.io/en/latest/cmd.html#cmd-run-debug

echo '[coverage debug sys]' > coverage_report.txt
coverage debug sys >> coverage_report.txt
echo -e "\n\n" >> coverage_report.txt

echo '[coverage debug config]' >> coverage_report.txt
coverage debug config >> coverage_report.txt
echo -e "\n\n" >> coverage_report.txt

echo '[coverage debug data]' >> coverage_report.txt
coverage debug data >> coverage_report.txt
echo -e "\n\n" >> coverage_report.txt

echo '[coverage debug premain]' >> coverage_report.txt
coverage debug premain >> coverage_report.txt
echo -e "\n\n" >> coverage_report.txt

echo '[coverage debug sys]' >> coverage_report.txt
coverage debug sys >> coverage_report.txt
echo -e "\n\n" >> coverage_report.txt

cat coverage_report.txt
