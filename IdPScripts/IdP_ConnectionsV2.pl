#!/usr/bin/perl -w
use strict;
use warnings;
use Sys::Hostname;


my ($asOfDate, $host, $mailReceiver, @mailRecips, $apacheprocsMax, $apacheprocsCount, $uptime, $timeStamp,
        $todaysdate, $apacheprocsfile, $freeMem, $timeStampPlus, $napTime, $tomcatMaxThreads,
        $idpPoolLDAPMinSize, $idpPoolLDAPMaxSize);


$host = hostname();
@mailRecips= ('ghall4@emory.edu');
$mailReceiver = 'ghall4@emory.edu';
$tomcatMaxThreads = 500;
$idpPoolLDAPMinSize = 20;
$idpPoolLDAPMaxSize = 120;

if($ARGV[0])
{ $apacheprocsMax = $ARGV[0];}
else { $apacheprocsMax = 300; }


$napTime = 5;
$todaysdate=`date +%Y%m%d`;
chop($todaysdate);

$apacheprocsfile = 'scriptOut/IdPConnections.txt';
open(WRITEFILE, ">>$apacheprocsfile");

$timeStampPlus = 0;


#while(1)
#{

  $apacheprocsCount = `ps -ef | grep http | wc -l`;
  $freeMem = `free -hm`;
  $uptime = `uptime`;

  chop($apacheprocsCount);

  #Tomcat IDP connections:
  #netstat -an | grep :9009
  my $TomcatIdPConnections = `netstat -an | grep :9009| wc -l`;
  #waiting:
  #netstat -an | grep :9009| grep TIME_WAIT
  my $TomcatIdPWaitConnections = `netstat -an | grep :9009| grep TIME_WAIT| wc -l`;

  #LDAP connections:
  #netstat -an | grep :636
  my $LDAPIdPConnections = `netstat -an | grep :636| wc -l`;
  #LDAP waiting:
  #netstat -an | grep :636| grep TIME_WAIT
  my $LDAPIdPWaitConnections = `netstat -an | grep :636| grep TIME_WAIT| wc -l`;

  $timeStamp = timeStamp();
  print "TimeStamp: $timeStamp\n";
  print "DATE:  $todaysdate \n";
  print "httpd procs: $apacheprocsCount at $uptime\n";
  print "$freeMem\n";
  print WRITEFILE "TimeStamp: $timeStamp\n";
  print WRITEFILE "DATE:  $todaysdate \n";
  print WRITEFILE "$freeMem\n";
  print WRITEFILE "httpd procs: $apacheprocsCount at $uptime\n";

  print "TomcatIdPConnections = $TomcatIdPConnections\n";
  print "TomcatIdPWaitConnections = $TomcatIdPWaitConnections\n";
  print "LDAPIdPConnections = $LDAPIdPConnections\n";
  print "LDAPIdPWaitConnections = $LDAPIdPWaitConnections\n";

  print WRITEFILE  "TomcatIdPConnections = $TomcatIdPConnections\n";
  print WRITEFILE  "TomcatIdPWaitConnections = $TomcatIdPWaitConnections\n";
  print WRITEFILE  "LDAPIdPConnections = $LDAPIdPConnections\n";
  print WRITEFILE  "LDAPIdPWaitConnections = $LDAPIdPWaitConnections\n";




    if( ($apacheprocsCount > $apacheprocsMax)  ||  ($TomcatIdPConnections >  $tomcatMaxThreads) || ($LDAPIdPConnections > $idpPoolLDAPMaxSize) )
    {
        $asOfDate =  dateTime();
        $timeStamp = timeStamp();

            #print "TIMESTAMP:      $timeStamp\n";
            #print "TIMESTAMPPLUS:  $timeStampPlus\n";

            print "\nWARNING: at $asOfDate\n";
            print "Apache processes on $host equal $apacheprocsCount\n";
            print "TomcatIdPConnections = $TomcatIdPConnections\n";
            print "TomcatIdPWaitConnections = $TomcatIdPWaitConnections\n";
            print "LDAPIdPConnections = $LDAPIdPConnections\n";
            print "LDAPIdPWaitConnections = $LDAPIdPWaitConnections\n";

            print WRITEFILE "\nWARNING: at $asOfDate\n";
            print WRITEFILE "Apache processes on $host equal $apacheprocsCount\n";
            print WRITEFILE "TomcatIdPConnections = $TomcatIdPConnections\n";
            print WRITEFILE "TomcatIdPWaitConnections = $TomcatIdPWaitConnections\n";
            print WRITEFILE "LDAPIdPConnections = $LDAPIdPConnections\n";
            print WRITEFILE "LDAPIdPWaitConnections = $LDAPIdPWaitConnections\n";

            #if($timeStamp > $timeStampPlus)
            #{
                $timeStampPlus = $timeStamp + 60;
                #print "SENDING MAIL\n";
                #sendMailAlert2($apacheprocsCount, $TomcatIdPConnections, $LDAPIdPConnections, $asOfDate, $host, @mailRecips);
                sendMailAlert2($apacheprocsCount, $TomcatIdPConnections, $LDAPIdPConnections, $asOfDate, $host, $mailReceiver);
            #}

    }

    #sleep($napTime);

#}




############################################################################################

sub sendMailAlert
{

      my ($apacheprocsCount, $asOfDate, $host, $mailRecips) = @_;



    open (MAIL, "|/usr/lib/sendmail -t");

      for(my $index=0; $index<@$mailRecips; $index++)
      {
            print MAIL "To: $$mailRecips[$index]\n";
            print MAIL "From: ghall4\@emory.edu\n";
            print MAIL "Subject: Apache processes on $host\n\n";
            print "Content-type: text/html\n\n";
            print MAIL "WARNING: $asOfDate Apache processes on $host equal $apacheprocsCount\n";
      }

     close (MAIL);

}


sub sendMailAlert2
{

        #my ($apacheprocsCount, $TomcatIdPConnections, $LDAPIdPConnections, $asOfDate, $host, @mailRecips) = @_;
        my ($apacheprocsCount, $TomcatIdPConnections, $LDAPIdPConnections, $asOfDate, $host, @mailReceiver) = @_;

        my $sendmail = '/usr/sbin/sendmail -t';

        my $replyTo = "From: ghall4\@emory.edu\n";
        my $subject = "Subject: IdP processes on $host\n\n";
        my $message = "WARNING: $asOfDate IdP processes on $host:\nApacheProcs = $apacheprocsCount\n, TomcatIdPConnections = $TomcatIdPConnections\n, LDAPIdPConnections = $LDAPIdPConnections\n";

        open(SENDMAIL, "|$sendmail") or warn "Cannot open $sendmail: $!";

        #for(my $index=0; $index<@$mailRecips; $index++)
        #{
            #my $sendTo = "To: $$mailRecips[$index]\n";
            my $sendTo = "To: $mailReceiver\n";

            # order is important for sendmail
            print SENDMAIL $sendTo;
            print SENDMAIL $replyTo;
            print SENDMAIL $subject;

            print SENDMAIL "Content-type: text/plain\n\n";
            print SENDMAIL $message;

        #}

        close (SENDMAIL);
}


sub dateTime
{
  my ($sec, $min, $hour, $mday, $month, $year, $wday, $yday, $isdst) = localtime();
  #my $thisday = qw(Sun Mon Tue Wed Thur Fri Sat)[(localtime)[6]];
  $month = qw(Jan Feb Mar Apr May June July Aug Sept Oct Nov Dec)[(localtime)[4]];
  # month: Jan=0, Feb=1, Mar=3, etc.
  $year = $year + 1900;

  if($mday < 10) {$mday = '0' . $mday};
  if($hour < 10) {$hour = '0' . $hour};
  if($min < 10) {$min = '0' . $min};
  if($sec < 10) {$sec = '0' . $sec};
  my $commentDateTime = "$year" . "$month". "$mday " . "$hour:$min:$sec";

  return   $commentDateTime;
}


sub timeStamp
{
    	my ($sec,$min,$hour,$mday,$month,$year,$wday,$yday,$isdst) = localtime;

    	$year = $year + 1900;
    	$month = $month + 1;            # Jan =0, Feb =1, etc.
    	if($sec < 10)   {$sec = "0" . $sec;}
    	if($min < 10)   {$min = "0" . $min;}
    	if($hour < 10)  {$hour = "0" . $hour;}
    	if($mday < 10)  {$mday = "0" . $mday;}
    	if($month < 10)   {$month = "0" . $month;}

    	my $timeStamp = "$year"."$month"."$mday". "$hour" . "$min" . "$sec";

    	return   $timeStamp;
}
