#### Kotaemon Project : a git subtree folder
#### Synchronisation commands

To pull the recent changes of your branch / or main branch, from the 'root' common project : https://github.com/dataforgoodfr/kotaemon#

```git subtree pull --prefix=rag_system/kotaemon https://github.com/dataforgoodfr/kotaemon.git [MY_BRANCH] --squash```

Contributing to the "root" project :

To contribute within your branch :

```git subtree push --prefix=rag_system/kotaemon  https://github.com/dataforgoodfr/kotaemon.git [MY_BRANCH]```

Replace [MY_BRANCH] with your branch version : 13_ecoskills_version, 13_sobriety_version ...

And if the changes are very generics => Do a Merge Request.

Be Careful ! All changes must be 'generics' to satisfy all projects ... (or explicitly written as '_example' )


###### Little Tips

Loccaly, you can create a git alias for the commands above ... Example (with the main branch of the subtree Project) for the pull command :

```git config --global alias.st-[MY_BRANCH]-pull 'git subtree pull --prefix=rag_system/kotaemon https://github.com/dataforgoodfr/kotaemon.git [MY_BRANCH] --squash' ```

and for the push command : 

```git config --global alias.st-[MY_BRANCH]-push 'git subtree push --prefix=rag_system/kotaemon  https://github.com/dataforgoodfr/kotaemon.git [MY_BRANCH] ' ```

Now, you can use these alias :


```git st-[MY_BRANCH]-pull ```

or 

```git st-[MY_BRANCH]-push ```
