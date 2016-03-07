# LswBareIPsDataBase
# v1.0
# Dimofinf, Inc
# # # # # # # # # #

import requests
import json
import xlsxwriter

apiurl = 'https://api.leaseweb.com/v1/bareMetals'
apikey = ''
headers = {"X-Lsw-Auth": apikey}
debug = 0

# Final file delivered
export_file = "servers.xlsx"

# Open XLSX file and adding sheets
workbook = xlsxwriter.Workbook(export_file)

# Formatting CELLS
cells_titles_format = workbook.add_format({'bold': True})
cells_titles_format.set_bg_color("#81BEF7")

worksheet_servers_details = workbook.add_worksheet("Servers IPs")

# Declaring Awesome variables for columns
baremetal_name_col = 0
baremetal_ip_col = 1
row_count = 1

# Set width for column
worksheet_servers_details.set_column(baremetal_name_col, baremetal_name_col, 16)
worksheet_servers_details.set_column(baremetal_ip_col, baremetal_ip_col, 20)

# Format to write ( row, column, content, format )
worksheet_servers_details.write(0, baremetal_name_col, "ServerName", cells_titles_format)
worksheet_servers_details.write(0, baremetal_ip_col, "ServerIP", cells_titles_format)

# Get list of servers
try:
    response = requests.get(apiurl, headers=headers)
    content = response.text
    content_json = json.loads(content)
    servers_number = len(content_json["bareMetals"])

    print("Please wait for a while until we get your IPs pool from leaseweb.")
    for count in range(servers_number):
        baremetal_json = content_json["bareMetals"][count]
        baremetal_id = baremetal_json['bareMetal']["bareMetalId"]
        baremetal_name = baremetal_json['bareMetal']["serverName"]

        if debug == 1:
            print("Generating information of : " + baremetal_name)

        percentage = 100 * (int(count)/int(servers_number))
        print("Percentage : %d %%" % (int(percentage)))

        # GET IPs information for each server
        apiurl_getip = 'https://api.leaseweb.com/v1/bareMetals/' + baremetal_id + '/ips'
        if debug == 1:
            print(apiurl_getip + "\n")

        ips_request = requests.get(apiurl_getip, headers=headers)
        ips_request_text = ips_request.text
        ips_request_json = json.loads(ips_request_text)
        ip_list = ips_request_json['ips']

        # Loop onto IPs list and filter it out in a clean list
        for z in ip_list:
            ipaddr = z['ip']['ip']
            servername = z['ip']['serverName']

            print(ipaddr)
            print(servername)
            print("===================")
            worksheet_servers_details.write(row_count, baremetal_name_col, servername)
            worksheet_servers_details.write(row_count, baremetal_ip_col, ipaddr)
            row_count += 1


except any:
    pass
# Close the final XLSX file
workbook.close()
print("\nDone")
