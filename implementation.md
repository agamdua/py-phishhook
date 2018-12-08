Our solution was based on detecting zero-day phishing links. 

This was the target that we had in mind we wanted to achieve. 

From a use case standpoint, we determined we wanted to try and trigger a website that URL Defense would incorrectly identify. 

To do this we chose how a website that is phishing would look and our design is based off of that thinking. 

A website that is disguised as malicious would want to pose as a non-malicious website. 
We broke down the process of identifying a website. 

Initially, after the email comes in, we screenshot the website. 

Next we check for logos of the website, since the website is posing as a non-malicious it will have some mechanism of identifying as the malicious website. 
This includes the logo. 
We used a screenshot service to screenshot the website and used LogoGrab to analyze the logo via an api request. 
We chose LogoGrab due to its robust reviews that we read online. 
Next a phishing website will want to look like the URL of the non-malicious website. 
So we analyze the URL, see if there are spaces or if the URL contains an acronym.

We also compare subdomains, to check if the website is part of a normal website and is just a false positive or not.

Like subdomain.google.com, this is owned by google and is a higher percentage change of not being malicious. 

Next we check out the certificate to see who is it issued to, is it the website who’s logo is displayed, or the website URL, and we compare the certificate issued to against popular websites.

The organization name, location, subject alternate names these are all verified here to analyze the subdomains.
Lastly, we compare the website URL to a database of top 1000 websites that we found publicly. Everything described here was compiled on one VM.  





Can you describe your implementation in detail? Why did you use this technology?
How does the theory relate to your implementation? What are your underlying assumptions?
What did you neglect and what simplifications have you made? What tools and methods did you use?
Why use these tools and methods?


6 Implementation

This section talks about the implementation of our PhishHook System. 
The code is open-sourced at: (should I make this a public repository? I don't see the harm. I would choose the relatively liberal BSD 3-clause license. To me this makes more sense than copy pasting the code into the appendix))

6.1 Choice of Technology

The goal of this system is to serve as a proof of concept of the effectiveness of the methods of a potential product while specifically staying away from building this as an actual product.

6.1.1 Execution Environment

Being clear about this line of thinking led us to choose Python as the language to implement the proof of concept - the teams familiarity with the language, along with dynamic typing would prove to be valuable in the speed of development, allowed us to ship a well-featured prototype while also allowing us to spend extra time on the actual research. Python also comes with a huge ecosystem of libraries which also allowed us to prototype faster, instead of reinventing the wheel in less featured ecosystems.

Python did come with one downside - we would now largely be restricted to run this code on the "server-side" as opposed to the client, one of which would be a web browser. While there is considerable work done to make Python run in the browser[1][2], this was tangential to the goals of the research phase of the potential product.

A browser plugin could have been a much more elegant User Experience, and we would have used JavaScript (TypeScript) to write that out. Apart from less familiarity on the team, this would have also ignored the demographic of users who use a desktop email client, which would have required server-side execution. A browser plugin could still be used as a client of this server-side process as an API accessed over HTTP.

6.1.2 External vendors

Maintaining the same theme of not reinventing the wheel we were able to leverage some commercial vendors:

1. screenshotlayer (insert reference)

From their website:
> Screenshotlayer is a lightweight REST API built to deliver high quality PNG, JPEG & GIF website screenshots at unparalleled speeds and through a simple interface.

We leveraged their free plan which allows 100 snapshots / month. We were able to do this by implementing a "frugal mode" toggle in the code, which did not use their API for taking a screenshot of a particular URL we were testing if we had already got a screenshot from them saved on disk.

2. LogoGrab (insert reference)

They describe themselves as:
>  the world’s highest-quality technology to identify logos in images and videos.

They have an startups / academia plan (https://www.logograb.com/startups) through which they granted us an API key for a limited set of brands till December 31st, 2018.

6.2 Implementation Steps

Definitions:
    1. Owner: the owner of the site is the actual owner you expect
    2. Masquerader: the entity which is pretending to be the owner of the
        content, and different from the owner of the phishing site.

Outline of approach:
    * We try to establish who an average user would think the owner of the
      site is by:
        * taking a screenshot of the site
        * detecting the logos on the site from the screenshot
        * determining if the site belongs to any of those entities
    * Checking information in the SSL cert
        * is there a cert?
        * is the issuee someone who we think should be the owner?
    * Checking URL
        * is the url on a domain that belongs to the proposed Owner

6.2.1 Identify Perceived Owner

The input to this phase is the URL of the website that the user wishes to 

The first part involves identification of the perceived Owner. For this, we interface with both the external vendors by asking Screenshotlayer to take a screenshot of the website in question. This image is then sent to LogoGrab via their API service to identify what major "brands" are on the site.
The output of this phase is a set of the brands detected.

6.2.2 Identify owner from URL and SSL certificate

The SSL certificate is read, any URL without one is immediately rejected as a
potential phishing attack. While debatable, this is also the model that browsers
are going in
(https://www.theverge.com/2018/2/8/16991254/chrome-not-secure-marked-http-encryption-ssl)

If there is a valid SSL certificate, we parse out the Issuer and the Issuee and
parse out names from the url of the site for potential owners.

6.2.3 Calculate Ownership legitimacy score

Here, we compare the information from the above section, that is the _perceived_
owner and the owner seen from the SSL certificate and URL. If the owner is
legitimate and has obtained a legitimate SSL certificate, these two should
match.

Here we use a Python library for fuzzy string matching that uses Levenshtein Distance for simple string comparisons under the hood.

A comparison of the items parsed out in 6.2.2 and the brands identified in 6.2.1
give us scores which we approximate as the confidence in ownership.

6.2.4 Downsides

There are many other variables we do not use that other research does use.

We do not currently output a single number as our "Confidence score". 


[1] https://www.transcrypt.org
[2] https://brython.info
