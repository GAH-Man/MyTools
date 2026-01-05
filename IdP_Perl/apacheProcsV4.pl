#!/usr/bin/perl -w
use strict;
use warnings;
use Sys::Hostname;


my ($asOfDate, $host, @mailRecips, $apacheprocsMax, $apacheprocsCount, $uptime, $timeStamp,
        $todaysdate, $apacheprocsfile, $freeMem, $timeStampPlus, $napTime);

$host = hostname();
@mailRecips= ('ghall4@emory.edu');
if($ARGV[0])
{ $apacheprocsMax = $ARGV[0];}
else { $apacheprocsMax = 300; }
$napTime = 5;
$todaysdate=`date +%Y%m%d`;
chop($todaysdate);

$apacheprocsfile = 'scriptOut/apachecprocs.txt';
open(WRITEFILE, ">>$apacheprocsfile");

$timeStampPlus = 0;

while(1)
{
    $apacheprocsCount = `ps -ef | grep http | wc -l`;
    $freeMem = `free -hm`;
    $uptime = `uptime`;

    chop($apacheprocsCount);

    if($apacheprocsCount > $apacheprocsMax)
    {
        $asOfDate =  dateTime();
        $timeStamp = timeStamp();

            #print "TIMESTAMP:      $timeStamp\n";
            #print "TIMESTAMPPLUS:  $timeStampPlus\n";

            print "\a\aWARNING: at $asOfDate Apache processes on $host equal $apacheprocsCount\n";
            print WRITEFILE "\a\aWARNING: at $asOfDate Apache processes on $host equal $apacheprocsCount\n";

            if($timeStamp > $timeStampPlus)
            {
                $timeStampPlus = $timeStamp + 60;
                #print "SENDING MAIL\n";
                sendMailAlert2($apacheprocsCount, $asOfDate, $host, \@mailRecips);
            }

    }

    print "$todaysdate httpd procs: $apacheprocsCount at $uptime";
    print "$freeMem\n";
    print WRITEFILE "$todaysdate httpd procs: $apacheprocsCount at $uptime";

    sleep($napTime);

}




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

        my ($apacheprocsCount, $asOfDate, $host, $mailRecips) = @_;

        my $sendmail = '/usr/sbin/sendmail -t';

        my $replyTo = "From: ghall4\@emory.edu\n";
        my $subject = "Subject: Apache processes on $host\n\n";
        my $message = "WARNING: $asOfDate Apache processes on $host equal $apacheprocsCount\n";

        open(SENDMAIL, "|$sendmail") or warn "Cannot open $sendmail: $!";

        for(my $index=0; $index<@$mailRecips; $index++)
        {
            my $sendTo = "To: $$mailRecips[$index]\n";

            # order is important for sendmail
            print SENDMAIL $sendTo;
            print SENDMAIL $replyTo;
            print SENDMAIL $subject;

            print SENDMAIL "Content-type: text/plain\n\n";
            print SENDMAIL $message;

        }

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
