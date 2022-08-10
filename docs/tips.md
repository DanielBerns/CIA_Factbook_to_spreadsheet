# Tips

## Amending the most recent commit message 
https://stackoverflow.com/questions/179123/how-to-modify-existing-unpushed-commit-messages

    git commit --amend -m "New commit message"

## Tagging
https://git-scm.com/book/en/v2/Git-Basics-Tagging

### Annotated Tags
Creating an annotated tag in Git is simple. The easiest way is to specify -a when you run the tag command:

    $ git tag -a v1.4 -m "my version 1.4"
    $ git tag
    v0.1
    v1.3
    v1.4

The -m specifies a tagging message, which is stored with the tag. If you don’t specify a message for an annotated tag, Git launches your editor so you can type it in.

### Sharing Tags
By default, the git push command doesn’t transfer tags to remote servers. You will have to explicitly push tags to a shared server after you have created them. This process is just like sharing remote branches — you can run git push origin <tagname>.

    $ git push origin v1.5
    Counting objects: 14, done.
    Delta compression using up to 8 threads.
    Compressing objects: 100% (12/12), done.
    Writing objects: 100% (14/14), 2.05 KiB | 0 bytes/s, done.
    Total 14 (delta 3), reused 0 (delta 0)
    To git@github.com:schacon/simplegit.git
     * [new tag]         v1.5 -> v1.5
 
 


















## Git story

    git log --pretty=oneline
    

