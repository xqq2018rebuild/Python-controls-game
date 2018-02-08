# 使用前 #
## 本地 ##
### 安装git 
  + linux
    +  > sudo apt-get install git 
    +  >sudo yum install git
  + windows: 
    + [Git 官网](https://git-scm.com/downloads)
    + [国内镜像](https://pan.baidu.com/s/1kU5OCOB?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=#list/path=%2Fpub%2Fgit)
### git 初次设置
```bash
    $ git config --global user.name "Your Name"
    $ git config --global user.email "email@example.com"
    $ mkdir git & cd git 
    $ git init 
```

## 远程仓库
### 创建步骤
1、创建SSH Key
```bash
$ ssh-keygen -t rsa -C "youremail@example.com"
```
如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。
2、添加公钥
登陆GitHub，打开“Account settings”，“SSH Keys”页面
然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容。为什么GitHub需要SSH Key呢？因为GitHub需要识别出你推送的提交确实是你推送的，而不是别人冒充的，而Git支持SSH协议，所以，GitHub只要知道了你的公钥，就可以确认只有你自己才能推送。
3、添加远程仓库
登陆GitHub，然后，在右上角找到“Create a new repo”按钮，创建一个新的仓库，在Repository name填入learngit，其他保持默认设置，点击“Create repository”按钮，就成功地创建了一个新的Git仓库。
目前，在GitHub上的这个learngit仓库还是空的，GitHub告诉我们，可以从这个仓库克隆出新的仓库，也可以把一个已有的本地仓库与之关联，然后，把本地仓库的内容推送到GitHub仓库。
4、关联远程仓库
```
$ git remote add origin git@github.com:ShenxCode/learngit.git
```
+ 远程库的名字就是origin，这是Git默认的叫法，也可以改成别的，但是origin这个名字一看就知道是远程库。
  5、本地库的所有内容推送到远程库上
```
$ git push -u origin master
Counting objects: 19, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (19/19), done.
Writing objects: 100% (19/19), 13.73 KiB, done.
Total 23 (delta 6), reused 0 (delta 0)
To git@github.com:michaelliao/learngit.git
 * [new branch]      master -> master
Branch master set up to track remote branch master from origin.
```
把本地库的内容推送到远程，用`git push`命令，实际上是把当前分支master推送到远程。
由于远程库是空的，我们第一次推送master分支时，加上了-u参数，Git不但会把本地的master分支内容推送的远程新的master分支，还会把本地的master分支和远程的master分支关联起来，在以后的推送或者拉取时就可以简化命令。
推送成功后，可以立刻在GitHub页面中看到远程库的内容已经和本地一模一样
6、本地修改后提交
```bash
$ git push origin master
```
把本地master分支的最新修改推送至GitHub，现在，你就拥有了真正的分布式版本库
**SSH警告**
当你第一次使用Git的clone或者push命令连接GitHub时，会得到一个警告：
```
The authenticity of host 'github.com (xx.xx.xx.xx)' can't be established.
RSA key fingerprint is xx.xx.xx.xx.xx.
Are you sure you want to continue connecting (yes/no)?
```
这是因为Git使用SSH连接，而SSH连接在第一次验证GitHub服务器的Key时，需要你确认GitHub的Key的指纹信息是否真的来自GitHub的服务器，输入yes回车即可。
Git会输出一个警告，告诉你已经把GitHub的Key添加到本机的一个信任列表里了：
```
Warning: Permanently added 'github.com' (RSA) to the list of known hosts.
```
这个警告只会出现一次，后面的操作就不会有任何警告了。
如果你实在担心有人冒充GitHub服务器，输入yes前可以对照GitHub的RSA Key的指纹信息是否与SSH连接给出的一致。
## 从远程仓库克隆
```
$ git clone git@github.com/ShenxCode/Python-controls-game
$ cd Python-controls-game
$ ls
```
如果有多个人协作开发，那么每个人各自从远程克隆一份就可以了。
你也许还注意到，GitHub给出的地址不止一个，还可以用如果有多个人协作开发，那么每个人各自从远程克隆一份就可以了。
你也许还注意到，GitHub给出的地址不止一个，还可以用这样https://github.com/ShenxCode/Python-controls-game的地址。实际上，Git支持多种协议，默认的git://使用ssh，但也可以使用https等其他协议。
使用https除了速度慢以外，还有个最大的麻烦是每次推送都必须输入口令，但是在某些只开放http端口的公司内部就无法使用ssh协议而只能用https。
**要克隆一个仓库，首先必须知道仓库的地址，然后使用git clone命令克隆。Git支持多种协议，包括https，但通过ssh支持的原生git协议速度最快**
# 使用中
## 添加一个文件并把文件提交到仓库
```bash
$ git add readme.md
$ git add readme.txt readme2.md
$ git commit -m  "本次提交说明"
```
## 查看当前仓库的状态
```bash
$ git status
```
+ modified 表示文件修改过了但是没有提交
+ untracked 表示文件从来没有添加过
## 查看文件修改了什么内容
```bash
$ git diff readme.md
```
+ `git diff HEAD -- readme.txt`查看工作区和版本库里面最新版本的区别
## 文件修改后提交修改
```bash
$ git add readme.md
$ git commit -m "修改了readme.md"
```
## 修改历史记录
```bash
$ git log 
```
+ `--pretty=oneline`参数作用为减少信息输出
+ `commit id`长长的一串数字，git 自动把每次提交的版本串成一条时间线
+ `HEAD`表示当前版本`HEAD^`表示上个版本`HEAD^^`上上个版本
  +` --graph` 命令可以看到分支合并图

## 把当前版本回退到上一版本
```bash
$ git reset --hard HEAD^
```
## 把当前版本回退到指定版本
```bash
$ git reset --hard 02134124
```
+ 数字表示用`git log`查到的commit id 的前几位数字就可以
## 命令记录
```bash
$ git reflog
```
+ 第一个数字为当前版本的commit id
## 撤消文件的修改
```bash
$ git checkout -- readme.txt
```
把readme.txt 文件在工作区的修改全部撤销，分两种情况
+ readme.txt自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态
+ readme.txt已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。
  总之，就是让这个文件回到最近一次git commit或git add时的状态。
+ 命令中`--` 很重要，没有的的话就变成“切换到另一个分支”的命令

`git reset HEAD file` 可以把暂存区的修改撤销掉（unstage），重新放回工作区
+ git reset命令既可以回退版本，也可以把暂存区的修改回退到工作区。当我们用HEAD时，表示最新的版本，然后在使用撤销工作区的修改
  若已经把修改提交到了仓库（不是远程仓库），可以适用版本回退撤销修改
## 删除
工作区文件删除
+ `git rm readme.md`把版本库的文件也删除
+ `git checkout -- readme.md`把误删的文件恢复到最新版本
  `git checkout`其实是用版本库里的版本替换工作区的版本，无论工作区是修改还是删除，都可以“一键还元”
  **命令`git rm`用于删除一个文件。如果一个文件已经被提交到版本库，那么你永远不用担心误删，但是要小心，你只能恢复文件到最新版本，你会丢失最近一次提交后你修改的内容。**
## 存储现场
```
$ git stash
```
可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作
## 恢复现场
```
$ git stash pop
```
## 查看远程仓库信息
```
$ git branch -D <name>
```
+ -v 显示更详细的信息，显示了可以抓取和推送的origin的地址。如果没有推送权限，就看不到push的地址
## 推送分支
推送分支，就是把该分支上的所有本地提交推送到远程库。推送时，要指定本地分支，这样，Git就会把该分支推送到远程库对应的远程分支上
```
$ git push origin master
```
如果要推送其他分支，比如dev，就改成
```
$ git push origin dev
```
但是，并不是一定要把本地分支往远程推送，那么，哪些分支需要推送，哪些不需要呢？
master分支是主分支，因此要时刻与远程同步；
dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步；
bug分支只用于在本地修复bug，就没必要推到远程了，除非老板要看看你每周到底修复了几个bug；
feature分支是否推到远程，取决于你是否和你的小伙伴合作在上面开发。
总之，就是在Git中，分支完全可以在本地自己藏着玩，是否推送，视你的心情而定
## 标签管理
### 总结
命令`git tag <name>`用于新建一个标签，默认为HEAD，也可以指定一个commit id
命令`git tag -a <tagname> -m "blablabla..."`可以指定标签信息；
命令`git tag -s <tagname> -m "blablabla..."`可以用PGP签名标签；
命令`git tag`可以查看所有标签。
命令`git push origin <tagname>`可以推送一个本地标签；
命令`git push origin --tags`可以推送全部未推送过的本地标签；
命令`it tag -d <tagname>`可以删除一个本地标签；
命令`git push origin :refs/tags/<tagname>`以删除一个远程标签。
### 查看所有标签
```
$ git tag
```
标签不是按时间顺序列出，而是按字母排序的
###创建标签
1、切换到需要打标签的分支上
```
$ git branch
* dev
  master
$ git checkout master
Switched to branch 'master'
```
2、创建标签
```
$ git tag <name>
```
### 指定commit id 打标签
1、找到历史commit id
```
$ git log --pretty=oneline --abbrev-commit
```
2、打标签
```
$ git tag v0.9 6224937
```
> git tag <name> <commit id> 

还可以创建带有说明的标签，用-a指定标签名，-m指定说明文字
```
$ git tag -a v0.1 -m "version 0.1 released" 3628164
```
还可以通过-s用私钥签名一个标
```
$ git tag -s v0.2 -m "signed version 0.2 released" fec145a
```
签名采用PGP签名，因此，必须首先安装gpg（GnuPG），如果没有找到gpg，或者没有gpg密钥对，就会报错,如果报错，请参考GnuPG帮助文档配置Key
### 查看标签信息
```
$ git show <tagname>
```
可以看到说明文字,可以看到PGP签名信息
### 删除标签
```
$ git tag -d v0.1
```
### 推送某个标签到远程
```
$ git push origin v1.0
```
一次性推送全部尚未推送到远程的本地标签
```
$ git push origin --tags
```
### 删除远程标签
1、先从本地删除
```
$ git tag -d v0.9
Deleted tag 'v0.9' (was 6224937)
```
2、从远程删除。删除命令也是push，但是格式如下：
```
$ git push origin :refs/tags/v0.9
To git@github.com:michaelliao/learngit.git
 - [deleted]         v0.9
```

## 分支管理
### 分支命令总结
查看分支：`git branch`
创建分支：`git branch <name>`
切换分支：`git checkout <name>`
创建+切换分支：`git checkout -b <name>`
合并某分支到当前分支：`git merge <name>`
删除分支：`git branch -d <name>`
分支合并图 `git log --graph --pretty=oneline --abbrev-commit`
禁用Fast forward合并`git merge --no-ff -m "merge with no-ff" <name>`
强行删除未合并的分支 `git branch -D <name>`
### 创建dev分支，然后切换到dev分支
```
$ git checkout -b dev
```
+ git checkout命令加上-b参数表示创建并切换，相当于以下两条命令
```
$ git branch dev
$ git checkout dev
```
### 查看当前分支
```
$ git branch
* dev
  master
```
git branch命令会列出所有分支，当前分支前面会标一个\*号
### 合并分支
我们把dev分支的工作成果合并到master分支上
```
$ git merge dev
Updating d17efd8..fec145a
Fast-forward
 readme.txt |    1 +
 1 file changed, 1 insertion(+)
```
git merge命令用于合并指定分支到当前分支。
注意到上面的Fast-forward信息，Git告诉我们，这次合并是“快进模式”，也就是直接把master指向dev的当前提交，所以合并速度非常快。
### 删除dev分支
```
$ git branch -d dev
```
### 解决冲突
master分支和dev分支进行了同一文件修改的不同提交
这种情况下，Git无法执行“快速合并”，只能试图把各自的修改合并起来，但这种合并就可能会有冲突
>$ git merge dev 

文件存在冲突，必须手动解决冲突后再提交。`git status`也可以告诉我们冲突的文件
手动修改冲突文件再次提交
### 分支的合并情况
```
$ git log --graph --pretty=oneline --abbrev-commit
```
### 禁用Fast forward合并
```
$ git merge --no-ff -m "merge with no-ff" dev
```
通常，合并分支时，如果可能，Git会用Fast forward模式，但这种模式下，删除分支后，会丢掉分支信息。
如果要强制禁用Fast forward模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息
因为本次合并要创建一个新的commit，所以加上-m参数，把commit描述写进去
### 修复BUG分支
1、保存现场
```
$ git stash
```
2、首先确定要在哪个分支上修复bug，假定需要在master分支上修复，就从master创建临时分支
```bash
$ git checkout master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 6 commits.
$ git checkout -b issue-101
Switched to a new branch 'issue-101'
```
3、修复后提交
```bash
$ git add readme.txt 
$ git commit -m "fix bug 101"
[issue-101 cc17032] fix bug 101
 1 file changed, 1 insertion(+), 1 deletion(-)
```
4、修复完成后，切换到master分支，并完成合并，最后删除issue-101分支
```
$ git checkout master
Switched to branch 'master'
Your branch is ahead of 'origin/master' by 2 commits.
$ git merge --no-ff -m "merged bug fix 101" issue-101
Merge made by the 'recursive' strategy.
 readme.txt |    2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
$ git branch -d issue-101
Deleted branch issue-101 (was cc17032).
```
5、回到dev分支干活了
```
$ git checkout dev
Switched to branch 'dev'
$ git status
# On branch dev
nothing to commit (working directory clean)
```
工作区是干净的，刚才的工作现场存到哪去了？用git stash list命令看看
```
$ git stash list
stash@{0}: WIP on dev: 6224937 add merge
```
工作现场还在，Git把stash内容存在某个地方了，但是需要恢复一下，有两个办法：
一是用git stash apply恢复，但是恢复后，stash内容并不删除，你需要用git stash drop来删除；
另一种方式是用git stash pop，恢复的同时把stash内容也删了
```
$ git stash pop
# On branch dev
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       new file:   hello.py
#
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git checkout -- <file>..." to discard changes in working directory)
#
#       modified:   readme.txt
#
Dropped refs/stash@{0} (f624f8e5f082f2df2bed8a4e09c12fd2943bdd40)
```
你可以多次stash，恢复的时候，先用git stash list查看，然后恢复指定的stash，用命令：
```
$ git stash apply stash@{0}
```
## git 知识
### 工作区
当前的文件目录
### 暂存区
`git add`命令实际上就是把要提交的所有修改放到暂存区（Stage），然后，执行`git commit`就可以一次性把暂存区的所有修改提交到分支
每次修改，如果不add到暂存区，那就不会加入到commit中，修改的内容也就提交不到版本中
### 分支作用
分支就是科幻电影里面的平行宇宙，当你正在电脑前努力学习Git的时候，另一个你正在另一个平行宇宙里努力学习SVN
分支在实际中有什么用呢？假设你准备开发一个新功能，但是需要两周才能完成，第一周你写了50%的代码，如果立刻提交，由于代码还没写完，不完整的代码库会导致别人不能干活了。如果等代码全部写完再一次提交，又存在丢失每天进度的巨大风险。
现在有了分支，就不用怕了。你创建了一个属于你自己的分支，别人看不到，还继续在原来的分支上正常工作，而你在自己的分支上干活，想提交就提交，直到开发完毕后，再一次性合并到原来的分支上，这样，既安全，又不影响别人工作
### 创建与合并分支
每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即master分支。HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，HEAD指向的就是当前分支。
一开始的时候，master分支是一条线，Git用master指向最新的提交，再用HEAD指向master，就能确定当前分支，以及当前分支的提交点。
每次提交，master分支都会向前移动一步，这样，随着你不断提交，master分支的线也越来越长。
当我们创建新的分支，例如dev时，Git新建了一个指针叫dev，指向master相同的提交，再把HEAD指向dev，就表示当前分支在dev上。

Git创建一个分支很快，因为除了增加一个dev指针，改改HEAD的指向，工作区的文件都没有任何变化！
不过，从现在开始，对工作区的修改和提交就是针对dev分支了，比如新提交一次后，dev指针往前移动一步，而master指针不变

假如我们在dev上的工作完成了，就可以把dev合并到master上。Git怎么合并呢？最简单的方法，就是直接把master指向dev的当前提交，就完成了合并

所以Git合并分支也很快！就改改指针，工作区内容也不变！
合并完分支后，甚至可以删除dev分支。删除dev分支就是把dev指针给删掉，删掉后，我们就剩下了一条master分支
### 分支策略
首先，master分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；
那在哪干活呢？干活都在dev分支上，也就是说，dev分支是不稳定的，到某个时候，比如1.0版本发布时，再把dev分支合并到master上，在master分支发布1.0版本；
你和你的小伙伴们每个人都在dev分支上干活，每个人都有自己的分支，时不时地往dev分支上合并就可以了。
###  抓取分支
多人协作时，大家都会往master和dev分支上推送各自的修改。
现在，模拟一个你的小伙伴，可以在另一台电脑（注意要把SSH Key添加到GitHub）或者同一台电脑的另一个目录下克隆：
```
$ git clone git@github.com:michaelliao/learngit.git
Cloning into 'learngit'...
remote: Counting objects: 46, done.
remote: Compressing objects: 100% (26/26), done.
remote: Total 46 (delta 16), reused 45 (delta 15)
Receiving objects: 100% (46/46), 15.69 KiB | 6 KiB/s, done.
Resolving deltas: 100% (16/16), done.
```
当你的小伙伴从远程库clone时，默认情况下，你的小伙伴只能看到本地的master分支。不信可以用git branch命令看看：
```
$ git branch
* master
```
现在，你的小伙伴要在dev分支上开发，就必须创建远程origin的dev分支到本地，于是他用这个命令创建本地dev分支：
```
$ git checkout -b dev origin/dev
```
现在，他就可以在dev上继续修改，然后，时不时地把dev分支push到远程：
```
$ git commit -m "add /usr/bin/env"
[dev 291bea8] add /usr/bin/env
 1 file changed, 1 insertion(+)
$ git push origin dev
Counting objects: 5, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 349 bytes, done.
Total 3 (delta 0), reused 0 (delta 0)
To git@github.com:michaelliao/learngit.git
   fc38031..291bea8  dev -> dev
```
你的小伙伴已经向origin/dev分支推送了他的提交，而碰巧你也对同样的文件作了修改，并试图推送：
```
$ git add hello.py 
$ git commit -m "add coding: utf-8"
[dev bd6ae48] add coding: utf-8
 1 file changed, 1 insertion(+)
$ git push origin dev
To git@github.com:michaelliao/learngit.git
 ! [rejected]        dev -> dev (non-fast-forward)
error: failed to push some refs to 'git@github.com:michaelliao/learngit.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Merge the remote changes (e.g. 'git pull')
hint: before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```
推送失败，因为你的小伙伴的最新提交和你试图推送的提交有冲突，解决办法也很简单，Git已经提示我们，先用git pull把最新的提交从origin/dev抓下来，然后，在本地合并，解决冲突，再推送：
```
$ git pull
remote: Counting objects: 5, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 3 (delta 0)
Unpacking objects: 100% (3/3), done.
From github.com:michaelliao/learngit
   fc38031..291bea8  dev        -> origin/dev
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream dev origin/<branch>

```
git pull也失败了，原因是没有指定本地dev分支与远程origin/dev分支的链接，根据提示，设置dev和origin/dev的链接：
```
$ git branch --set-upstream dev origin/dev
Branch dev set up to track remote branch dev from origin.
```
再pull：
```
$ git pull
Auto-merging hello.py
CONFLICT (content): Merge conflict in hello.py
Automatic merge failed; fix conflicts and then commit the result.
```
这回git pull成功，但是合并有冲突，需要手动解决，解决的方法和分支管理中的解决冲突完全一样。解决后，提交，再push：
```
$ git commit -m "merge & fix hello.py"
[dev adca45d] merge & fix hello.py
$ git push origin dev
Counting objects: 10, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (6/6), 747 bytes, done.
Total 6 (delta 0), reused 0 (delta 0)
To git@github.com:michaelliao/learngit.git
   291bea8..adca45d  dev -> dev
 
```
因此，多人协作的工作模式通常是这样：
首先，可以试图用`git push origin branch-name`推送自己的修改；
如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
如果合并有冲突，则解决冲突，并在本地提交；
没有冲突或者解决掉冲突后，再用`git push origin branch-name`推送就能成功！
如果git pull提示“no tracking information”，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream branch-name origin/branch-name`。
这就是多人协作的工作模式，一旦熟悉了，就非常简单。
**小结**
查看远程库信息，使用`git remote -v`；
本地新建的分支如果不推送到远程，对其他人就是不可见的；
从本地推送分支，使用`git push origin branch-name`，如果推送失败，先用git pull抓取远程的新提交；
在本地创建和远程分支对应的分支，使用`git checkout -b branch-name origin/branch-name`，本地和远程分支的名称最好一致；
建立本地分支和远程分支的关联，使用`git branch --set-upstream branch-name origin/branch-name`；
从远程抓取分支，使用git pull，如果有冲突，要先处理冲突。
### 标签
发布一个版本时，我们通常先在版本库中打一个标签（tag），这样，就唯一确定了打标签时刻的版本。将来无论什么时候，取某个标签的版本，就是把那个打标签的时刻的历史版本取出来。所以，标签也是版本库的一个快照
tag就是一个让人容易记住的有意义的名字，它跟某个commit绑在一起
### 使用github
我们一直用GitHub作为免费的远程仓库，如果是个人的开源项目，放到GitHub上是完全没有问题的。其实GitHub还是一个开源协作社区，通过GitHub，既可以让别人参与你的开源项目，也可以参与别人的开源项目。
在GitHub出现以前，开源项目开源容易，但让广大人民群众参与进来比较困难，因为要参与，就要提交代码，而给每个想提交代码的群众都开一个账号那是不现实的，因此，群众也仅限于报个bug，即使能改掉bug，也只能把diff文件用邮件发过去，很不方便。
但是在GitHub上，利用Git极其强大的克隆和分支功能，广大人民群众真正可以第一次自由参与各种开源项目了。
如何参与一个开源项目呢？比如人气极高的bootstrap项目，这是一个非常强大的CSS框架，你可以访问它的项目主页https://github.com/twbs/bootstrap，点“Fork”就在自己的账号下克隆了一个bootstrap仓库，然后，从自己的账号下clone：
```
git clone git@github.com:michaelliao/bootstrap.git
```
一定要从自己的账号下clone仓库，这样你才能推送修改。如果从bootstrap的作者的仓库地址git@github.com:twbs/bootstrap.git克隆，因为没有权限，你将不能推送修改。
Bootstrap的官方仓库twbs/bootstrap、你在GitHub上克隆的仓库my/bootstrap，以及你自己克隆到本地电脑的仓库，他们的关系就像下图显示的那样：

如果你想修复bootstrap的一个bug，或者新增一个功能，立刻就可以开始干活，干完后，往自己的仓库推送。
如果你希望bootstrap的官方库能接受你的修改，你就可以在GitHub上发起一个pull request。当然，对方是否接受你的pull request就不一定了。
如果你没能力修改bootstrap，但又想要试一把pull request，那就Fork一下我的仓库：https://github.com/michaelliao/learngit，创建一个your-github-id.txt的文本文件，写点自己学习Git的心得，然后推送一个pull request给我，我会视心情而定是否接受。
小结
在GitHub上，可以任意Fork开源仓库；
自己拥有Fork后的仓库的读写权限；
可以推送pull request给官方仓库来贡献代码。
### 自定义git
+ 让git显示颜色`$ git config --global color.ui true`
+ 使用别名 `$ git config --global alias.<别名> <命令>`
#### 忽略特殊文件
有些时候，你必须把某些文件放到Git工作目录中，但又不能提交它们，比如保存了数据库密码的配置文件啦，等等，每次git status都会显示Untracked files ...，有强迫症的童鞋心里肯定不爽。
好在Git考虑到了大家的感受，这个问题解决起来也很简单，在Git工作区的根目录下创建一个特殊的.gitignore文件，然后把要忽略的文件名填进去，Git就会自动忽略这些文件。
不需要从头写.gitignore文件，GitHub已经为我们准备了各种配置文件，只需要组合一下就可以使用了。所有配置文件可以直接在线浏览：https://github.com/github/gitignore
忽略文件的原则是：
忽略操作系统自动生成的文件，比如缩略图等；
忽略编译生成的中间文件、可执行文件等，也就是如果一个文件是通过另一个文件自动生成的，那自动生成的文件就没必要放进版本库，比如Java编译产生的.class文件；
忽略你自己的带有敏感信息的配置文件，比如存放口令的配置文件。
举个例子：
假设你在Windows下进行Python开发，Windows会自动在有图片的目录下生成隐藏的缩略图文件，如果有自定义目录，目录下就会有Desktop.ini文件，因此你需要忽略Windows自动生成的垃圾文件：
```
#Windows
Thumbs.db
ehthumbs.db
Desktop.ini
```
然后，继续忽略Python编译产生的.pyc、.pyo、dist等文件或目录：
```
#Python
*.py[cod]
*.so
*.egg
*.egg-info
dist
build
```
加上你自己定义的文件，最终得到一个完整的.gitignore文件，内容如下：
```
#Windows
Thumbs.db
ehthumbs.db
Desktop.ini

#Python 
*.py[cod]
*.so
*.egg
*.egg-info
dist
build

# My configurations
db.ini
deploy_key_rsa
```
最后一步就是把.gitignore也提交到Git，就完成了！当然检验.gitignore的标准是git status命令是不是说working directory clean。
使用Windows的童鞋注意了，如果你在资源管理器里新建一个.gitignore文件，它会非常弱智地提示你必须输入文件名，但是在文本编辑器里“保存”或者“另存为”就可以把文件保存为.gitignore了。
有些时候，你想添加一个文件到Git，但发现添加不了，原因是这个文件被.gitignore忽略了：
```
$ git add App.class
The following paths are ignored by one of your .gitignore files:
App.class
Use -f if you really want to add them.
```
如果你确实想添加该文件，可以用-f强制添加到Git：
```
$ git add -f App.class
```
或者你发现，可能是.gitignore写得有问题，需要找出来到底哪个规则写错了，可以用git check-ignore命令检查：
```
$ git check-ignore -v App.class
.gitignore:3:*.class    App.class
```
Git会告诉我们，.gitignore的第3行规则忽略了该文件，于是我们就可以知道应该修订哪个规则。
**小结**
忽略某些文件时，需要编写.gitignore；
.gitignore文件本身要放到版本库里，并且可以对.gitignore做版本管理！
#### 配置别名
有没有经常敲错命令？比如git status？status这个单词真心不好记。
如果敲git st就表示git status那就简单多了，当然这种偷懒的办法我们是极力赞成的。
我们只需要敲一行命令，告诉Git，以后st就表示status：
```
$ git config --global alias.st status
```
好了，现在敲git st看看效果。
当然还有别的命令可以简写，很多人都用co表示checkout，ci表示commit，br表示branch：
```
$ git config --global alias.co checkout
$ git config --global alias.ci commit
$ git config --global alias.br branch
```
以后提交就可以简写成：
```
$ git ci -m "bala bala bala..."
```
--global参数是全局参数，也就是这些命令在这台电脑的所有Git仓库下都有用。
在撤销修改一节中，我们知道，命令git reset HEAD file可以把暂存区的修改撤销掉（unstage），重新放回工作区。既然是一个unstage操作，就可以配置一个unstage别名：
```
$ git config --global alias.unstage 'reset HEAD'
```
当你敲入命令：
```
$ git unstage test.py
```
实际上Git执行的是：
```
$ git reset HEAD test.py
```
配置一个git last，让其显示最后一次提交信息：
```
$ git config --global alias.last 'log -1'
```
这样，用git last就能显示最近一次的提交：
```
$ git last
commit adca45d317e6d8a4b23f9811c3d7b7f0f180bfe2
Merge: bd6ae48 291bea8
Author: Michael Liao <askxuefeng@gmail.com>
Date:   Thu Aug 22 22:49:22 2013 +0800

    merge & fix hello.py
```
甚至还有人丧心病狂地把lg配置成了：
```
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```
来看看git lg的效果：

为什么不早点告诉我？别激动，咱不是为了多记几个英文单词嘛！
配置文件
配置Git的时候，加上--global是针对当前用户起作用的，如果不加，那只针对当前的仓库起作用。
配置文件放哪了？每个仓库的Git配置文件都放在.git/config文件中：
```
$ cat .git/config 
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
    ignorecase = true
    precomposeunicode = true
[remote "origin"]
    url = git@github.com:michaelliao/learngit.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
[alias]
    last = log -1
```
别名就在[alias]后面，要删除别名，直接把对应的行删掉即可。
而当前用户的Git配置文件放在用户主目录下的一个隐藏文件.gitconfig中：
```
$ cat .gitconfig
[alias]
    co = checkout
    ci = commit
    br = branch
    st = status
[user]
    name = Your Name
    email = your@email.com
```
配置别名也可以直接修改这个文件，如果改错了，可以删掉文件重新通过命令配置。

#### 搭建git服务器
在远程仓库一节中，我们讲了远程仓库实际上和本地仓库没啥不同，纯粹为了7x24小时开机并交换大家的修改。
GitHub就是一个免费托管开源代码的远程仓库。但是对于某些视源代码如生命的商业公司来说，既不想公开源代码，又舍不得给GitHub交保护费，那就只能自己搭建一台Git服务器作为私有仓库使用。
搭建Git服务器需要准备一台运行Linux的机器，强烈推荐用Ubuntu或Debian，这样，通过几条简单的apt命令就可以完成安装。
假设你已经有sudo权限的用户账号，下面，正式开始安装。
第一步，安装git：
```
$ sudo apt-get install git
```
第二步，创建一个git用户，用来运行git服务：
```
$ sudo adduser git
```
第三步，创建证书登录：
收集所有需要登录的用户的公钥，就是他们自己的id_rsa.pub文件，把所有公钥导入到/home/git/.ssh/authorized_keys文件里，一行一个。
第四步，初始化Git仓库：
先选定一个目录作为Git仓库，假定是/srv/sample.git，在/srv目录下输入命令：
```
$ sudo git init --bare sample.git
```
Git就会创建一个裸仓库，裸仓库没有工作区，因为服务器上的Git仓库纯粹是为了共享，所以不让用户直接登录到服务器上去改工作区，并且服务器上的Git仓库通常都以.git结尾。然后，把owner改为git：
```
$ sudo chown -R git:git sample.git
```
第五步，禁用shell登录：
出于安全考虑，第二步创建的git用户不允许登录shell，这可以通过编辑/etc/passwd文件完成。找到类似下面的一行：
```
git:x:1001:1001:,,,:/home/git:/bin/bash
```
改为：
```
git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
```
这样，git用户可以正常通过ssh使用git，但无法登录shell，因为我们为git用户指定的git-shell每次一登录就自动退出。
第六步，克隆远程仓库：
现在，可以通过git clone命令克隆远程仓库了，在各自的电脑上运行：
```
$ git clone git@server:/srv/sample.git
Cloning into 'sample'...
warning: You appear to have cloned an empty repository.
```
剩下的推送就简单了。
管理公钥
如果团队很小，把每个人的公钥收集起来放到服务器的/home/git/.ssh/authorized_keys文件里就是可行的。如果团队有几百号人，就没法这么玩了，这时，可以用Gitosis来管理公钥。
这里我们不介绍怎么玩Gitosis了，几百号人的团队基本都在500强了，相信找个高水平的Linux管理员问题不大。
管理权限
有很多不但视源代码如生命，而且视员工为窃贼的公司，会在版本控制系统里设置一套完善的权限控制，每个人是否有读写权限会精确到每个分支甚至每个目录下。因为Git是为Linux源代码托管而开发的，所以Git也继承了开源社区的精神，不支持权限控制。不过，因为Git支持钩子（hook），所以，可以在服务器端编写一系列脚本来控制提交等操作，达到权限控制的目的。Gitolite就是这个工具。
这里我们也不介绍Gitolite了，不要把有限的生命浪费到权限斗争中。
小结
搭建Git服务器非常简单，通常10分钟即可完成；
要方便管理公钥，用Gitosis；
要像SVN那样变态地控制权限，用Gitolite。







