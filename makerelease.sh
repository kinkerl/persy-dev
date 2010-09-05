#!/bin/bash

# Current working dir
workdir="`pwd`"


gpgkey="AF005C40"
version=""

make_build()
{
    echo "Running configure and make"
    ./configure && make
    version="`cat usr/share/persy/assets/VERSION`"
}

continue_release()
{
    echo ""
    echo -n "Continue releasing persy-${version} ? (y/n): "
    read answer
    if [ "$answer" != "y" ]; then
        echo "Exit."
        exit 0
    fi

    # git tag & push
    git tag -f $version
    git push origin master --tags
}

publish_doc()
{
    echo "Begin publishing documentation..."
    git commit -am "autocommit uncommited changes"
    #preparing temp
    rm -fr /tmp/_build/html
    mkdir -p /tmp/_build/html
    mv usr/share/doc/persy/* /tmp/_build/html/
	
    #prepare gh-pages and remove existing stuff
    git checkout gh-pages
    git pull origin gh-pages
    rm -rf *
	
    #make the changes
    cp -r /tmp/_build/html/* .
    git add .
    git commit -am "autoupdated documentation"
    git push origin gh-pages
	
    #switch back to master
    git checkout master
    mkdir -p  usr/share/doc/persy/ 
    mv /tmp/_build/html/* usr/share/doc/persy/ 
    echo "Documentation publishing finished. The HTML pages are at http://kinkerl.github.com/persy/"

}

build_src_package()
{
    echo "Building debian source package..."
    echo -n "Checking for debuild... "
    if [ -z `which debuild 2> /dev/null` ]; then
        echo -e "no"
        exit 1
    else
        echo -e "yes"
    fi
    debuild -S -sa -k${gpgkey} -i.git -I.git
    echo "Build finished; Get the debian package at ../persy_${version}.tar.gz"
}

build_deb_package()
{
    echo "Start building debian package..."
    echo -n "Checking for debuild... "
    if [ -z `which debuild 2> /dev/null` ]; then
        echo -e "no"
        exit 1
    else
        echo -e "yes"
    fi   
    debuild -i.git -I.git
    echo "Build finished; Get the debian package at ../persy_${version}_all.deb"
}

build_tar_package()
{
    echo "Start building tar.gz package..."
    mkdir ${workdir}/persy-${version}
    make clean
    rm Makefile
    cp -rf * ${workdir}/persy-${version}
    cd ${workdir}
    tar cvzf persy-${version}.tar.gz persy-${version}
    rm -rf persy-${version}
    echo "Build finished; Get the tar.gz package at ${PWD}/persy-${version}.tar.gz"
}

upload_source_changes()
{
    echo "Uploading source changes to ppa"
    dput -f  ppa:tmassassin/ppa ../persy_${version}_source.changes
}

test_persy()
{
    #pychecker does some tests and checks for errors in the source code
    echo "pychecker tests..."
    if [ -z `which pychecker` ]; then
        echo -e "Skip (pychecker not installed)"
    else
        pychecker usr/share/persy/lib/*.py
    fi
    echo "pyflakes tests..."

    #same with pyflakes
    if [ -z `which pyflakes` ]; then
        echo -e "Skip (pyflakes not installed)"
    else
        pyflakes usr/share/persy/lib/*.py
    fi

}

#run
opt=$1
case $opt in
    "release")
            make_build
            continue_release
            publish_doc
            build_src_package
            upload_source_changes
            echo -n "Finaly released persy-$version."
            ;;
    "public-doc")
            make_build
            publish_doc
            ;;
    "makedeb")  
            make_build
            build_deb_package
            ;;
    "maketar")
            make_build
            build_tar_package
            ;;
    "test")  
            test_persy
            ;;
    *)
        echo "Usage: `pwd`/$0 {release|makedeb|maketar|public-doc|test}"
        exit 1
        ;;
esac

echo "Done."
exit 0
