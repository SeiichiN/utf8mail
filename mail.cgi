#!/usr/bin/perl

use strict;
use utf8;
use Encode;
use MIME::Base64;
use Net::SMTP;
use CGI;

############### 確認項目 ########################
# 引数を取り込む(ここは変更しないで、formをこれに合わせてね)
my $cgi = CGI::new();
# お客様のメールアドレスを取り込む
my $mail_from = $cgi->param('address');
# お客様のコメントを取り込む
my $message = $cgi->param('body');
utf8::decode($message) unless utf8::is_utf8($message);
# お客様の名前を取り込む
my $mail_from_name = $cgi->param('name');
utf8::decode($mail_from_name) unless utf8::is_utf8($mail_from_name);

############# 設定 #############################
# メール送信に使うSMTPサーバーと、ポート番号、送信者のドメインを設定する。
# サーバー管理者に確認してね。
my $smtp_server = 'Owner.Zino-PC';
my $smtp_port = '25';
my $smtp_helo = 'Owner.Zino-PC';

########## あなたが設定する項目 #####################
# あなたの名前をメールアドレスを記述する。
# お客様のコメントがメールとなって、あなたのもとに届く。
my $mail_to_name = '糠山';
my $mail_to = 'se-ichi@Owner.Zino-PC';

# メールの件名を設定する。
# この件名であなたのもとに届くよ。
my $subject = 'コメントが届いてます。';

# メール送信後に「戻る」でどこにリンクするか？
my $modoru = './';

# メールヘッダを作成する。
# from、to、件名共にMIME-Header(UTF-8)へエンコードします。
my $mail_header;

# 送信者名、送信者のメールアドレスを、
# From: 送信者名 <送信者メールアドレス> 形式へ変換する。
$mail_header = make_name_addr('From:',$mail_from_name,$mail_from);

# 宛名、宛先のメールアドレスを、
# To: 宛名 <宛先メールアドレス> 形式へ変換する。
$mail_header .= make_name_addr('To:',$mail_to_name,$mail_to);

# 件名をMIMEエンコードする。
$mail_header .= 'Subject: '.encode('MIME-Header',$subject)."\n";

# UTF-8とbase64エンコードを使う事を明記します。
$mail_header .= "MIME-Version: 1.0\n";
$mail_header .= "Content-type: text/plain; charset=UTF-8\n";
$mail_header .= "Content-Transfer-Encoding: base64\n";

# メールヘッダの終わり。(これ以降は本文となります。)
$mail_header .= "\n";

# SMTPでメールを送る。
my $SMTP=Net::SMTP->new($smtp_server, Port=>$smtp_port, Hello=>$smtp_helo);
if (!$SMTP) { die "Error : Can not connect to mail server.\n"; }
$SMTP->mail($mail_from);
$SMTP->to($mail_to);
$SMTP->data();
$SMTP->datasend($mail_header);
$SMTP->datasend(encode_base64(encode('utf8', $message)));
$SMTP->dataend();
$SMTP->quit;

print<<"EOM";
Content-type: text/html

<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>メール送信</title>
</head>
<body>
メールを送信しました。<br><br>
<a href="$modoru">戻る</a>
</body></html>
EOM

exit;

# 名前とメールアドレスから、name_addr形式のフォーマットを作るサブルーチン。
sub make_name_addr {
# 引数を受け取る。
my ($mail_direction,$mail_name,$mail_address) = @_;
# 末尾にスペースを追加して"From: "または "To: "を作る。
my $name_addr = $mail_direction.' ';

# 名前(送信者名または宛名)が設定されているか調べる。
if ($mail_name ne "") {
# 名前が設定されていたら、
# 名前をMIMEエンコードして、末尾にスペースを追加する。
$name_addr .= encode('MIME-Header',$mail_name).' ';
}
# メールアドレスを追加する。
return ($name_addr .= '<'.$mail_address.">\n");
}

########################################################
# 参考（というか引用元）
# perlでUnicode(UTF-8)で書かれたメールを送信する方法
# http://www.fantasy.jp/~hibernal/document/20100217.htm
########################################################
