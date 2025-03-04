<h1 style="margin-bottom: 50px;"> [Tutorial] Finding vulnerabilities in a Cybersecurity model using BooLEVARD</h1>
<p>
    In this tutorial, we will explore a small Boolean model designed to simulate different cybersecurity scenarios. The model consists of nodes representing key components of a cybersecurity system, and the goal of this tutorial is to evaluate how different conditions and guidelines affect the overall security state of the system.
</p>
<p>
    The model includes the following nodes: <br><br>
    <ul>
        <li> Inputs: 
            <code style="font-size: 14px; margin-bottom: 100px">Security_Policies</code>,
            <code style="font-size: 14px; margin-bottom: 100px">User_Education</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Network_Monitoring</code>, and
            <code style="font-size: 14px; margin-bottom: 100px">Security_Patches</code>.<br><br>
        <li> Internal nodes:
            <code style="font-size: 14px; margin-bottom: 100px">Backups</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Malware</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Firewall</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Unauthorized_Access</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Exploits</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Antivirus</code>,
            <code style="font-size: 14px; margin-bottom: 100px">Strong_Password</code>,
            <code style="font-size: 14px; margin-bottom: 100px">TwoFactAut</code>, and
            <code style="font-size: 14px; margin-bottom: 100px">Phishing_Attack</code>.<br><br>
        <li> Output nodes:
            <code style="font-size: 14px; margin-bottom: 100px">Security_State</code>.
    </ul>

</p>

![Network Visual](https://github.com/farinasm/boolevard/blob/main/tutorial/security_model.png)

