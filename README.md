# utf8mail
mail of utf-8 ( Perl )

smtp.gmail.comのアカウントを使ってメール発信できます。  
2段階認証ではないgmail.comのアカウントが必要です。  

モジュールとして、  
Email::MIME  
Email::Sender::Simple  
Email::Sender::Transport::SMTP::TLS  
をインストールする必要があるかもしれません。  

その場合は、ubuntuなら、以下のようにすればインストールできます。  
$ sudo cpan <Enter>  
cpan[1]> install Email::MIME <Enter>  
cpan[2]> （以下、同様）  
cpan[4]> q <Enter>  

ローカル環境でWebサイト制作の勉強をしていて、メール発信のテストを
したくなった場合、ローカル環境にはsmtpサーバが動いていないことが
多いと思います。

そのとき、これを使うこともひとつの選択肢だと思います。

mail_old.cgi は、出発点となったコードです。一応残しておきます。
これを改良して、今回のコードができました。

また、XAMPPのsendmailを使って、smtp.gmailサーバーに向けてメールを発信することもできます。  
その場合も、このoldコードを改良して作りました。

