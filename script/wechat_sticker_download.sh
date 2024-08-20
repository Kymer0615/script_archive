#!/bin/bash

# reference: https://blog.jogle.top/2022/08/14/macos-wechat-sticker-dump/
cur_dir=$(pwd);
cd ~/Library/Containers/com.tencent.xinWeChat/Data/Library/Application\ Support/com.tencent.xinWeChat/*/*/Stickers/;
tar_dir=$(pwd);
cd $cur_dir  ;
cp "${tar_dir}/fav.archive" "./temp/"
mv ./temp/fav.archive ./temp/fav.archive.plist;
plutil -convert xml1 ./temp/fav.archive.plist;