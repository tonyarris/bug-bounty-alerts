bug-bounty-alerts
===

A script to scan HackerOne bug bounty scopes and notify via email when they change.

## Setup


- Add a `h1_device_id` and `__Host-session` value to `./requests_template/headers.json`. You can find this value by visiting a scope page, e.g. [https://hackerone.com/spotify?type=team](https://hackerone.com/spotify?type=team) and inspecting cookies in your browser's Developer Tools pane. No login is required.
- Rename the `requests_template` folder to `requests`
- Browse the [HackerOne Directory](https://hackerone.com/directory/programs?order_direction=DESC&order_field=resolved_report_count) and add your desired bounty program names to the `targets.txt` file, one per line. This name must match exactly the URL directory of the program home. E.g. to add the AT&T program, first visit the program page at [https://hackerone.com/att?type=team](https://hackerone.com/att?type=team) and note the directory name in the URL. In this case, we need to add the directory name `att` to our `targets.txt` file
- Add your email SMTP settings to `secrets_template.yml` and rename the file to `secrets.yml`
- Add your recipient first name(s) and email(s) to `contacts.txt`, one per line, separated by a space
- Customise the body of the notification email by editing `message.txt`
- `pip install PyYAML`
- Run `init.py` to populate the `responses/` folder with existing bounty scopes
- Run `main.py` to populate `tmp/` and diff the current scopes against the previous 
- Automate with `cron` or similar to check the scopes at your desired frequency. I recommend not doing this too frequently to avoid spamming HackerOne and/or getting your IP blocked.