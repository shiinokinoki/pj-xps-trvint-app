SYSTEM_MESSAGE = """You are an assistant to respond to email inquiries for a travel planning agency.
You will act as an assistant to correctly and accurately structure and understand the content of inquiry emails sent to travel planning agencies and create a response.
These inquiry e-mails are sent by the intermediary company with the information of the actual travel customers.
You are responsible for structuring and organizing the information of the brokerage firm and the customer from the contents of the inquiry mail in order to propose the best travel plan to the customer through the intermediary company, and creating an email that prompts the intermediary company to reply to you regarding the missing information.
"""


HUMAN_MESSAGE_EXT_DATA = """You have just received an inquiry email with your information.

Email content
--------
The content of the email is as follows

```
{email_content}
```

My Request
--------
{request}


Output format
--------
{format_instructions}

Here is your an attention point:
1. The final output structured data SHOULD NOT be ambiguous.
2. DO NOT make assumptions on your own, and structure only the information that can be explicitly determined from the information in the mail.
3. Items that could not be confirmed should be set to None.
"""

agt_info_ext_req = 'Please extract and structure information of the intermediary company.'
cst_info_ext_req = 'Please extract and structure information of the customer.'
all_info_ext_req = 'Please extract and structure information of the intermediary company and the customer.'

HUMAN_MESSAGE_GEN_MAIL = """You have just received an inquiry email with your information.

Email content
--------
The content of the email is as follows

```
{email_content}
```

This e-mail lacked some information necessary to answer this inquiry.
Please suggest an e-mail to the recipient asking for this missing information in addition, as a form of reply to the above e-mail.

The missing information is as follows:
{lacked_info}

Here is your an attention point:
1. The person you are e-mailing is an important business partner, so please consider your reply in the form of a rude business e-mail!

Body of reply e-mail: \n
"""


EMAIL_CONTENT_SAMPLE = """
agt name : PeacockTravel, inquiry date : 2023-03-17 00:00:00
sub : PEACOCK TRAVEL - Denmark  "Five-star Experiences" all over Japan
body : Hi Koji

Thanks for your mail. I  would like to have a talk with you as we do have a booking for May 20th May - 4th June.
It's a family with 2 adults and 1 teenage daughter of 15 years.
Could you call me tomorrow please.

Thanks/Best Regards

[cid:image001.png@01D95834.B92DF200]<http://www.discoverytravel.dk/>
[cid:image002.png@01D95834.B92DF200]
Estelle Torp
CEO / Owner
[Et billede, der indeholder tekst  Automatisk genereret beskrivelse]<https://www.peacocktravel.dk/>
Hellerupvej 51C, 2900 Hellerup, Denmark
Office +45 39 62 61 61, Direct +45 88 77 53 00
[cid:image004.jpg@01D95834.B92DF200]<https://www.facebook.com/DiscoveryTravelDanmark/>  [cid:image005.png@01D95834.B92DF200] <https://www.instagram.com/discoverytraveldanmark/>
torp@discoverytravel.dk<mailto:torp@discoverytravel.dk> torp@peacocktravel.dk<mailto:torp@peacocktravel.dk>
"""