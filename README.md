PhishHook
=========

Phishing detection for dummies.


### Current state

< 200 lines of code currently.


Downloads a screenshot of a website, and saves it to a file of the same name as
the url. 

Does not send it for logo detection to  LogoGrab / Google yet.

Fetches info for SSL cert `issued_by` and `issued_to`. Does not do anything from
this information yet.

Does not analyze URL yet.

### In operation

*Note* The screenshot API I am using rate limits to 100/month then charges.
I have added a `FRUGAL_MODE` feature that checks if the screnshit for the URL is
already saved, then it doesn't screenshit again via the API.

```
$ SCREENSHOT_ACCESS_KEY=<redacted> python main.py
[FRUGAL MODE ON] hibshman.net.jpeg already downloaded, skipping capture
SSL Certificate issued to <hibshman.net> by <Go Daddy Secure Certificate Authority - G2>
```

```
$ SCREENSHOT_ACCESS_KEY=<redacted> python main.py
[FRUGAL MODE ON] nyuclubs.atspace.cc.jpeg already downloaded, skipping capture
No SSL cert found for <nyuclubs.atspace.cc>, GTFO and contact your site adminitstrator
```
