# NetBackUp-Splunk-Addon
A none-official Splunk add-on for NetBackUp by Veritas.

Current version - v1.0.0

The app collects security logs using the REST API of NetBackUp, writes them as new Splunk events in JSON format, and saves an index for future executions to avoid writing duplicated events into Splunk.

# Installing the NetBackUp TA
To Install the Splunk add-on straight to your Splunk deployment simply follow these few simple steps:

  - Download the file named: 'TA-netbackup-log-fetcher_1_0_0_export.tgz'.
  - follow this link to the Splunk documentation regarding installing new add-ons in various ways: https://docs.splunk.com/Documentation/AddOns/released/Overview/Installingadd-ons
  - Installing using CLI:
      1. Upload the .tgz file to your Splunk server under location: "/tmp/" ;
         On a distributed SE set-up use your Splunk Manager deployment server for this task.
      2. Unzip the .tgz file to the desited location - "tar xvzf splunk_package_name.tgz -C $SPLUNKHOME/etc/apps";
         For distributed SE use this path - "$SPLUNKHOME/etc/deployment-apps".
      3. For single instance users - 
            * you should now see your new Splunk app ready for use in your Splunk GUI.
      4. For distributed SE - 
            * navigate to your Splunk Manager deployment GUI.
            * Under 'Settings' click 'Forwarder Management'.
            * In the search box type the name of the app - 'TA-netbackup-log-fetcher'.
            * Click 'Edit'.
            * Using the '+' button assign the app to all of your desired Splunk server classes (make sure to check 'Restart Splunkd').
            * Wait for the Splunk deployments associated with this server class to load back up, you shall now see the app available in the associated deployment's GUI.

# Data inputs set-up
To set up a new data input for this app you will need an API key, your NetBackUp hostname, and a local path for the app to store it's check-point index on, aswell as a paeameter that toggles SSL verification On/Off.
You can also set up a proxy server, of course.

# Contact me
In any case regarding this app - bug fixes, feature request and more; contact me through LinkedIn, Github, or via email at amitngithub23@gmail.com .
