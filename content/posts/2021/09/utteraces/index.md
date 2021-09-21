---
title: "From Disqus to Utterances"
date: 2021-09-21
tags: ["Hugo", "GitHub Pages", "Blog", "Utterances"]
categories: ["Hugo"]
draft: false
---

I've been using Disqus to implement the comments feature, but the free plan was not good because of the ads.
So I migrated to Utterances which implements the comment feature using GitHub Issues.

<!--more-->

# Background

Hugo's Harbor theme, which I used in this blog, quickly implemented the comment function by setting `disqusShortName` in `config.toml`.
However, since I'm using Disqus free plan, I've started to get ads sometimes.
It was not so beautiful, so I decided to move to Utterances, which I've been interested in for a while.

Utterances is a lightweight comment widget implemented using GitHub Issues.

# How to implement

## Prepare a GitHub repository for comments

Since I deployed this blog based on `github.com/kakeami/blog`, there was no need to create a new repository by using GitHub Issues in the `kakeami/blog` repository.
However, mixing the original issues and comments seemed inconvenient, so I created a `github.com/kakeami/blog-comments` repository for storing comments.

## Install Utterances

I installed Utterances from GitHub App as instructed.

## Embed the script tag

I needed to embed the following script tag where I wanted to put the comment field.

```html
<script src="https://utteranc.es/client.js"
    repo="kakeami/blog-comments"
    issue-term="pathname"
    label="comment"
    theme="github-light"
    crossorigin="anonymous"
    async>
</script>
```

Please refer to the official page of Utterances for the definition of each setting value.


I was not familiar with Hugo at all, so I had to research where to embed it.
After `grep`ing the source code, I found that Disqus is embedded in `/themes/harbor/layouts/_default/single.html` in Harbor.

```html
 {{ define "main" }}
   <div class="container" role="main">
     <article class="article" class="blog-post">
       {{ partial "toc.html" . }}

       {{ if .Params.tags }}
         <div class="blog-tags">
           {{ range .Params.tags }}
             <a
               href="{{ "" | absLangURL }}tags/{{ . | urlize }}{{ if $.Site.Params.uglyurls }}.html{{ else }}/{{ end }}"
               >{{ . }}</a
             >&nbsp;
           {{ end }}
         </div>
       {{ end }}
     </article>
     {{ if and (gt .WordCount 400) (.Param "backtotop") }}
       {{ partial "backtotop.html" . }}
       <button onclick="topFunction()" id="backtotopButton">
         <em class="fa fa-angle-up"></em>
       </button>
     {{ end }}
     {{ if  (not (isset .Params "disable_comments")) }}
       {{ partial "disqus.html" . }}
     {{ end }}
   </div>
 {{ end }}
```

It seems that `single.html` (called Single Page Templates) is a template applied to individual articles.

According to [レイアウト用のテンプレートの種類を理解する](https://maku77.github.io/hugo/layout/template-types.html), Hugo employs Single Page Templates in the following order of precedence in:

- `/layouts/{type}/{layout}.html`
- `/layouts/{section}/{layout}.html`
- `/layouts/{type}/single.html`
- `/layouts/{section}/single.html`
- `/layouts/_default/single.html`
- `/themes/{theme}/layouts/{type}/{layout}.html`
- `/themes/{theme}/layouts/{section}/{layout}.html`
- `/themes/{theme}/layouts/{type}/single.html`
- `/themes/{theme}/layouts/{section}/single.html`
- `/themes/{theme}/layouts/_default/single.html`

To make it consistent with Harbor's structure, I decided to override it by creating `/layouts/_default/single.html`.

```html
 {{ define "main" }}
   <div class="container" role="main">
     <article class="article" class="blog-post">
       {{ partial "toc.html" . }}

       {{ if .Params.tags }}
         <div class="blog-tags">
           {{ range .Params.tags }}
             <a
               href="{{ "" | absLangURL }}tags/{{ . | urlize }}{{ if $.Site.Params.uglyurls }}.html{{ else }}/{{ end }}"
               >{{ . }}</a
             >&nbsp;
           {{ end }}
         </div>
       {{ end }}
     </article>
     {{ if and (gt .WordCount 400) (.Param "backtotop") }}
       {{ partial "backtotop.html" . }}
       <button onclick="topFunction()" id="backtotopButton">
         <em class="fa fa-angle-up"></em>
       </button>
     {{ end }}

     <script src="https://utteranc.es/client.js"
         repo="kakeami/blog-comments"
         issue-term="pathname"
         label="comment"
         theme="github-light"
         crossorigin="anonymous"
         async>
     </script>

   </div>
 {{ end }}
```

That's it!

# Impressions

Very useful and cool.
I'm glad I learned something about Hugo's design.

# Reference

- [utterances](https://utteranc.es/)
- [Hugo's Lookup Order](https://gohugo.io/templates/lookup-order/#examples-layout-lookup-for-regular-pages)
- [レイアウト用のテンプレートの種類を理解する](https://maku77.github.io/hugo/layout/template-types.html)
