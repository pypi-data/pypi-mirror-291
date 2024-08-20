!function(){"use strict";{const i=_.template(`<div>
<% if (useAvatars && avatarHTML) { %>
 <%= avatarHTML %>
<% } %>
<% if (fullname) { %>
 <span class="title"><%- fullname %></span>
 <span class="description">(<%- username %>)</span>
<% } else { %>
 <span class="title"><%- username %></span>
<% } %>
</div>`);RB.RelatedUserSelectorView=Djblets.RelatedObjectSelectorView.extend({searchPlaceholderText:gettext("Search for users..."),initialize(e){Djblets.RelatedObjectSelectorView.prototype.initialize.call(this,_.defaults({selectizeOptions:{searchField:["fullname","username"],sortField:[{field:"fullname"},{field:"username"}],valueField:"username"}},e)),this._localSitePrefix=e.localSitePrefix||"",this._useAvatars=!!e.useAvatars},renderOption(e){return i(_.extend({useAvatars:this._useAvatars},e))},loadOptions(e,i){var a={fullname:1,"only-fields":"avatar_html,fullname,id,username","only-links":"","render-avatars-at":"20"};0!==e.length&&(a.q=e),$.ajax({type:"GET",url:""+SITE_ROOT+this._localSitePrefix+"api/users/",data:a,success(e){i(e.users.map(e=>({avatarHTML:e.avatar_html[20],fullname:e.fullname,id:e.id,username:e.username})))},error(...e){console.error("User query failed",e),i()}})}})}{const a=_.template(`<div>
 <span class="title"><%- name %></span>
</div>`);RB.RelatedRepoSelectorView=Djblets.RelatedObjectSelectorView.extend({searchPlaceholderText:gettext("Search for repositories..."),initialize(e){Djblets.RelatedObjectSelectorView.prototype.initialize.call(this,_.defaults({selectizeOptions:{searchField:["name"],sortField:[{field:"name"}],valueField:"name"}},e)),this._localSitePrefix=e.localSitePrefix||""},renderOption(e){return a(e)},loadOptions(e,i){var a={"only-fields":"name,id"};0!==e.length&&(a.q=e),$.ajax({type:"GET",url:""+SITE_ROOT+this._localSitePrefix+"api/repositories/",data:a,success:e=>{i(e.repositories.map(e=>({name:e.name,id:e.id})))},error:(...e)=>{console.error("Repository query failed",e),i()}})}})}{const t=_.template(`<div>
 <span class="title"><%- name %> : <%- display_name %></span>
</div>`);RB.RelatedGroupSelectorView=Djblets.RelatedObjectSelectorView.extend({searchPlaceholderText:gettext("Search for groups..."),initialize(e){Djblets.RelatedObjectSelectorView.prototype.initialize.call(this,_.defaults({selectizeOptions:{searchField:["name","display_name"],sortField:[{field:"name"},{field:"display_name"}],valueField:"name"}},e)),this._localSitePrefix=e.localSitePrefix||"",this._inviteOnly=e.inviteOnly,this._showInvisible=e.showInvisible},renderOption(e){return t(e)},loadOptions(e,i){var a={"only-fields":"invite_only,name,display_name,id",displayname:1};0!==e.length&&(a.q=e),this._inviteOnly&&(a["invite-only"]="1"),this._showInvisible&&(a["show-invisible"]="1"),$.ajax({type:"GET",url:""+SITE_ROOT+this._localSitePrefix+"api/groups/",data:a,success:e=>{i(e.groups.map(e=>({name:e.name,display_name:e.display_name,id:e.id,invite_only:e.invite_only})))},error:(...e)=>{console.error("Group query failed",e),i()}})}})}}.call(this);
