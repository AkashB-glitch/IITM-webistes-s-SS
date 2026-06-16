# IIT Madras Subdomain Security Risk Report

**Date:** 2024-07-30

## 1. Introduction
This report summarizes the security posture of IIT Madras subdomains based on a comprehensive security pipeline execution. The pipeline involved subdomain discovery, port scanning, screenshot capture, vision scanning, and data analysis to identify potential security risks and vulnerabilities.

## 2. Summary of Findings
The security scan identified a significant number of subdomains associated with IIT Madras. A considerable portion of these subdomains exhibited various security concerns, ranging from non-standard open ports, "Down" or "Error" statuses indicating operational issues, to instances of WAF (Web Application Firewall) retries which could suggest attempted malicious activity or misconfigurations. Several subdomains also presented SSL Certificate Warnings, indicating potential issues with secure communication.

**Key Observations:**
*   A substantial number of subdomains are either unreachable (DNS Resolution Failure, Connection Error/Refused, Timeout) or returning error codes (404, 502, 503, 403, 401). These "down" or "error" sites could be unmaintained, deprecated, or potentially compromised, posing a risk of shadow IT or unpatched vulnerabilities.
*   Multiple subdomains expose port 3306 (MySQL), which is a non-standard port to be exposed directly to the internet without proper protection, potentially exposing database services.
*   Several sites show "SSL Certificate Warnings," which can erode user trust and expose data to interception if not properly addressed.
*   A few sites recorded WAF retries, which might indicate attempts to bypass security measures or misconfigured WAF rules.

## 3. Highly Suspicious Sites

The following subdomains are flagged as highly suspicious due to critical issues such as non-standard open ports (specifically 3306), down/error statuses, or recorded WAF retries. These sites warrant immediate investigation and remediation.

| Domain                       | Status Category          | Status Code             | Open Ports             | WAF Retries | Suspicion Reason                               |
|------------------------------|--------------------------|-------------------------|------------------------|-------------|------------------------------------------------|
| alumni.iitm.ac.in            | Error                    | 404                     | [80, 443]              | 0           | Error status (404 Not Found)                   |
| acservices.iitm.ac.in        | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| alumni.doms.iitm.ac.in       | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| appdev.onlinedegree.iitm.ac.in| Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| archive.iitm.ac.in           | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| asean.iitm.ac.in             | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| asuldap.iitm.ac.in           | Down                     | Connection Error        | [22, 80, 443, 8080]    | 1           | Down status (Connection Error) & WAF Retries   |
| backend.seek.onlinedegree.iitm.ac.in | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| biomimicry.iitm.ac.in        | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| cammd.iitm.ac.in             | Down                     | DNS Resolution Failure  | [21, 22, 80, 443, 3306]| 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| cec.iitm.ac.in               | Down                     | DNS Resolution Failure  | [21, 80, 443, 3306]    | 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| ceet.iitm.ac.in              | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| cessa.iitm.ac.in             | Down                     | DNS Resolution Failure  | [21, 22, 80, 443, 3306]| 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| chennai36.iitm.ac.in         | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| cmt.respark.iitm.ac.in       | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| cryoem.iitm.ac.in            | Down                     | DNS Resolution Failure  | [21, 22, 80, 443, 3306]| 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| d3.iitm.ac.in                | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| datacommons.iitm.ac.in       | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| dsai.iitm.ac.in              | Down                     | DNS Resolution Failure  | [22, 80, 443]          | 0           | Down status (DNS Resolution Failure)           |
| e-verify.acservices.iitm.ac.in| Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| elearn.iitm.ac.in            | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| events.respark.iitm.ac.in    | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| ext01ldap.iitm.ac.in         | Down                     | Connection Refused      | [22]                   | 0           | Down status (Connection Refused)               |
| fw.respark.iitm.ac.in        | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| ge-uat.iitm.ac.in            | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| giftshop.iitm.ac.in          | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| hc-uat.iitm.ac.in            | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| heritage.iitm.ac.in          | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| hmis-app.iitm.ac.in          | Down                     | Connection Error        | []                     | 1           | Down status (Connection Error) & WAF Retries   |
| ikollege.iitm.ac.in          | Error                    | 404                     | [22, 80, 443, 8080, 8443]| 0           | Error status (404 Not Found)                   |
| impactstories.iitm.ac.in     | Error                    | 404                     | [80, 443, 8080, 8443]  | 0           | Error status (404 Not Found)                   |
| keepitflowing.alumni.iitm.ac.in| Down                     | DNS Resolution Failure  | [22, 80, 443]          | 0           | Down status (DNS Resolution Failure)           |
| leap.respark.iitm.ac.in      | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| mailx1.iitm.ac.in            | Down                     | Connection Refused      | [22, 80, 3306]         | 0           | Down status (Connection Refused) & Port 3306 exposed |
| mailx2.iitm.ac.in            | Active                   | 200                     | [22, 80, 443, 3306]    | 0           | Port 3306 exposed                              |
| mailx3.iitm.ac.in            | Down                     | Connection Refused      | [22, 80, 3306]         | 0           | Down status (Connection Refused) & Port 3306 exposed |
| mailx4.iitm.ac.in            | Active                   | 200                     | [22, 80, 443, 3306]    | 0           | Port 3306 exposed                              |
| moodle.respark.iitm.ac.in    | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| mst.iitm.ac.in               | Down                     | DNS Resolution Failure  | [21, 80, 443, 3306]    | 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| ncaht.iitm.ac.in             | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| nipta.iitm.ac.in             | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| nptelonlinecourses.iitm.ac.in| Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| oir.iitm.ac.in               | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| pallava.iitm.ac.in           | Active                   | 200                     | [22, 80, 443, 3306]    | 0           | Port 3306 exposed                              |
| paramvidya.iitm.ac.in        | Warning                  | 403                     | [80, 443, 3306]        | 0           | Access Denied (403 Forbidden) & Port 3306 exposed |
| placements.onlinedegree.iitm.ac.in | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| r2d2.iitm.ac.in              | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| riselab.iitm.ac.in           | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| scoringtool.code.iitm.ac.in  | Error                    | 502                     | [80, 443]              | 1           | Error status (502 Bad Gateway) & WAF Retries   |
| shaastramag-uat.iitm.ac.in   | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| shaastramag.iitm.ac.in       | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| sites.ee.iitm.ac.in          | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| ssan.iitm.ac.in              | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| smtp.iitm.ac.in              | Down                     | Timeout                 | [22]                   | 1           | Down status (Timeout) & WAF Retries            |
| smtp1.iitm.ac.in             | Down                     | Timeout                 | [22]                   | 1           | Down status (Timeout) & WAF Retries            |
| smtp2.iitm.ac.in             | Down                     | Timeout                 | [22]                   | 1           | Down status (Timeout) & WAF Retries            |
| student.onlinedegree.iitm.ac.in| Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| tcoe.iitm.ac.in              | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| tlc2.iitm.ac.in              | Down                     | DNS Resolution Failure  | [22, 80, 443, 3306]    | 0           | Down status (DNS Resolution Failure) & Port 3306 exposed |
| vanakkamkashi.iitm.ac.in     | Down                     | Timeout                 | []                     | 1           | Down status (Timeout) & WAF Retries            |
| vpn.iitm.ac.in               | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| web.respark.iitm.ac.in       | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| wmtai.iitm.ac.in             | Down                     | DNS Resolution Failure  | [22, 80, 443]          | 0           | Down status (DNS Resolution Failure)           |
| wmail.iitm.ac.in             | Active                   | 200                     | [22, 80, 443, 3306]    | 0           | Port 3306 exposed                              |
| www.alumni.doms.iitm.ac.in   | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| www.archive.iitm.ac.in       | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| www.backend.seek.onlinedegree.iitm.ac.in | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| www.biomimicry.iitm.ac.in    | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| www.chennai36.iitm.ac.in     | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| www.incubation.iitm.ac.in    | Down                     | DNS Resolution Failure  | [80]                   | 0           | Down status (DNS Resolution Failure)           |
| www.kashitamil.iitm.ac.in    | Error                    | 503                     | [443]                  | 1           | Error status (503 Service Unavailable) & WAF Retries |
| www.leap.respark.iitm.ac.in  | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| www.respark.iitm.ac.in       | Warning                  | 403                     | [80, 443]              | 0           | Access Denied (403 Forbidden) - potential WAF interaction |
| www.shaastramag.iitm.ac.in   | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| www.tcoe.iitm.ac.in          | Down                     | DNS Resolution Failure  | []                     | 0           | Down status (DNS Resolution Failure)           |
| www.vanakkamkashi.iitm.ac.in | Down                     | Timeout                 | []                     | 1           | Down status (Timeout) & WAF Retries            |
| yaari.iitm.ac.in             | Down                     | DNS Resolution Failure  | [80, 443]              | 0           | Down status (DNS Resolution Failure)           |
| yrf.iitm.ac.in               | Warning                  | 403                     | [80, 443]              | 0           | Access Denied (403 Forbidden)                  |

## 4. Other Observations

### SSL Certificate Warnings
A significant number of subdomains are reporting "SSL Certificate Warning". While not always critical, these warnings can indicate misconfigurations, expired certificates, or self-signed certificates, which can impact trust and secure communication.

Example domains with SSL Certificate Warnings:
*   `accounts.iitm.ac.in`
*   `ae.iitm.ac.in`
*   `asu-preprod.iitm.ac.in`
*   `asu-preprodb.iitm.ac.in`
*   `biofoundry.iitm.ac.in`
*   `cifil.iitm.ac.in`
*   `dev.iitm.ac.in`
*   `hr-api-uat.iitm.ac.in`
*   `hr-uat.iitm.ac.in`
*   `instispace.iitm.ac.in`
*   `internalrecruit.iitm.ac.in`
*   `ioas.iitm.ac.in`
*   `icsrpis.iitm.ac.in`
*   `iitmprwa.iitm.ac.in`
*   `inup.iitm.ac.in`
*   `ip.iitm.ac.in`
*   `isea-isap2026.iitm.ac.in`
*   `ishmt.iitm.ac.in`
*   `ivrf.iitm.ac.in`
*   `isroiitmcoe.iitm.ac.in`
*   `jaljeevaninnovate.iitm.ac.in`
*   `jam.iitm.ac.in`
*   `jeeadv.iitm.ac.in`
*   `match.iitm.ac.in`
*   `math.iitm.ac.in`
*   `maxrap.iitm.ac.in`
*   `mbsfacapp.iitm.ac.in`
*   `mcsc.iitm.ac.in`
*   `mea.iitm.ac.in`
*   `mech.iitm.ac.in`
*   `mems.iitm.ac.in`
*   `metallurgy.iitm.ac.in`
*   `mme.iitm.ac.in`
*   `mtechadm.iitm.ac.in`
*   `naksha.iitm.ac.in`
*   `nccrd.iitm.ac.in`
*   `nctb.iitm.ac.in`
*   `nfapt.iitm.ac.in`
*   `nptelonlinecourses1.iitm.ac.in`
*   `nss.iitm.ac.in`
*   `nsm.iitm.ac.in`
*   `ntcpwc.iitm.ac.in`
*   `odei.iitm.ac.in`
*   `oldcourses.iitm.ac.in`
*   `parentconnect.iitm.ac.in`
*   `pbl.biotech.iitm.ac.in`
*   `photos.iitm.ac.in`
*   `physics.iitm.ac.in`
*   `posh.iitm.ac.in`
*   `quantum.iitm.ac.in`
*   `ramoodle.iitm.ac.in`
*   `rbcdsai.iitm.ac.in`
*   `rbg.iitm.ac.in`
*   `recruit.iitm.ac.in`
*   `redcap.iitm.ac.in`
*   `rekhicentersoh.iitm.ac.in`
*   `research.iitm.ac.in`
*   `rtis.iitm.ac.in`
*   `rutag.iitm.ac.in`
*   `saif.iitm.ac.in`
*   `scaleai.iitm.ac.in`
*   `semantic.iitm.ac.in`
*   `skillsacademy.iitm.ac.in`
*   `smart.iitm.ac.in`
*   `sports.iitm.ac.in`
*   `sustainability.iitm.ac.in`
*   `tcf.iitm.ac.in`
*   `techkids.iitm.ac.in`
*   `tgh.iitm.ac.in`
*   `thearc.iitm.ac.in`
*   `tlc.iitm.ac.in`
*   `touchlab.iitm.ac.in`
*   `uay.iitm.ac.in`
*   `uatv2.joyofgiving.alumni.iitm.ac.in`
*   `tulais.iitm.ac.in`
*   `ugadmissions.iitm.ac.in`
*   `vanavani.iitm.ac.in`
*   `web.iitm.ac.in`
*   `icsris.iitm.ac.in`
*   `webopac.iitm.ac.in`
*   `wfapi-uat.iitm.ac.in`
*   `womensforum.iitm.ac.in`
*   `workflow-api.iitm.ac.in`
*   `workflow-elearn.iitm.ac.in`
*   `www.ee.iitm.ac.in`
*   `www.iitm.ac.in`
*   `www.techkids.iitm.ac.in`
*   `xtic.iitm.ac.in`

## 5. Recommendations

Based on the findings, the following recommendations are provided to enhance the security posture of IIT Madras subdomains:

*   **Decommission or Secure "Down" and "Error" Sites:** Investigate all subdomains with "Down" or "Error" statuses. For sites that are no longer needed, ensure they are properly decommissioned to prevent them from being exploited in the future (e.g., DNS hijacking). For sites that should be operational, troubleshoot and restore their functionality.
*   **Review Exposed Ports:** Immediately investigate subdomains exposing non-standard critical ports like 3306 (MySQL). Database servers should generally not be directly accessible from the internet. Implement strict firewall rules and consider placing these services behind a robust application gateway or VPN.
*   **Address SSL Certificate Warnings:** Promptly address all SSL Certificate Warnings. This includes renewing expired certificates, ensuring correct certificate installation, and using trusted Certificate Authorities. This helps maintain secure communication and user trust.
*   **Investigate WAF Retries:** Analyze logs for subdomains showing WAF retries. While WAFs are designed to block malicious traffic, a high number of retries could indicate persistent attacks or misconfigured rules that are overly aggressive or not effectively blocking threats.
*   **Regular Security Audits:** Implement a schedule for regular, automated security scans and manual penetration testing to continuously identify and remediate vulnerabilities.
*   **Asset Inventory and Management:** Maintain an up-to-date inventory of all subdomains and their operational status. This ensures that all public-facing assets are known and regularly monitored.
*   **Implement Strong Security Policies:** Enforce policies for secure development, deployment, and maintenance of all web applications and services.

## 6. Conclusion
The security scan provided valuable insights into the current state of IIT Madras subdomains. While many sites appear operational, the presence of numerous "Down" or "Error" sites, exposed critical ports, and SSL warnings highlight areas requiring immediate attention. By addressing the identified risks and implementing the recommended security measures, IIT Madras can significantly enhance its cybersecurity posture and protect its digital assets and brand reputation.
