#!/usr/bin/perl
# あなたの環境に合わせる ex.C:\xampp\perl\perl.exe 

use strict;
use warnings;

use utf8;
use Email::MIME;
use Email::MIME::Creator;
use Encode;
use Email::Sender::Simple 'sendmail';
use Email::Sender::Transport::SMTP::TLS;
use Try::Tiny;
use CGI;

my $cgi = CGI::new();

# ========= 設定項目 ==================
# フォームからデータを受け取る
# name, address, body をフォームに合わせて変更する。
#
my $from_name = $cgi->param('name');
my $from_mail = $cgi->param('address');
my $comment = $cgi->param('body');

# メールを届けてもらうメールアドレスを設定する
#
my $to_name = 'Momonga Nazarick';  # このメールを届けてもらいたい名前
my $to_mail = 'ains@nazarick.com'; # このメールを受け取りたいメールアドレス

# smtp.gmail.com の設定
#
my $mailhost = 'smtp.gmail.com';
my $mailport = 587;
my $mail_username = 'XXXXXXXX@gmail.com'; # あなたのgmailアカウント
my $mail_password = 'YYYYYYYY';           # あなたのパスワード
### 注）このコードは2段階認証に対応していません。
###     2段階認証でないアカウントを取得してください。

# メール送信後に「戻る」でどこにリンクするか？
my $modoru = './';

# ============== 設定項目ここまで ========================

# -------------------------------------------
# フォームからのデータのチェック
# 文字コードがUTF-8でなかった場合、UTF-8に変換する
#
utf8::decode($from_name) unless utf8::is_utf8($from_name);
utf8::decode($comment) unless utf8::is_utf8($comment);

# ------------------------------------------------
# メールの体裁
#
# あなたに届くメールの表題
my $subject = 'コメントが届いています。';

# メール本文（お客様の情報とコメントがここに入る）
my $contents;
$contents .= 'お名前：' . $from_name . "\n";
$contents .= 'メールアドレス：' . $from_mail . "\n";
$contents .= 'コメント：' . $comment . "\n";
# --------------------------------------------------

# "（あなたの名前）" <XXXXXXX@gmail.com> という文字列を作っている。
my $to_name_mail = '"' . $to_name . '"<' . $to_mail . '>';

# -----------------------------------------------------
### utf-8を使う場合
# -----------------------------------------------------
my $email = Email::MIME->create(
    header_str => [
        From    => $from_mail,
        To      => $to_name_mail,
        Subject => $subject,
    ],
    attributes => {
        content_type => 'text/plain',
        charset      => 'UTF-8',
        encoding     => 'base64',
	},
    body_str => $contents,
    );

my $transport = Email::Sender::Transport::SMTP::TLS->new(
    host => $mailhost,
    port => $mailport,
    username => $mail_username,
    password => $mail_password
    );

try {
    sendmail( $email, {transport => $transport} );
} catch {
    my $error = $_ ;  warn $error->message;
};

my $html = <<"EOM";
Content-type: text/html

<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
</head>
<body>
メールを送信しました。<br>
<p><a href=" $modoru ">戻る</a></p>
</body>
</html>
EOM
    
print $html;
