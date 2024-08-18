from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import debug_toolbar
from project.sparta_582d4dfd84.sparta_154d7a64c0 import qube_cde64080a5
from project.sparta_582d4dfd84.sparta_92b6b326c8 import qube_9ab238a798
from project.sparta_582d4dfd84.sparta_d60c4466c2 import qube_6c85283e81
from project.sparta_582d4dfd84.sparta_ca74f77b94 import qube_30d3f5b738
from project.sparta_c2313b36e9.sparta_b51a5d620f import qube_11486cd76c
from project.sparta_c2313b36e9.sparta_329cd4f244 import qube_1f4b0baf84
from project.sparta_c2313b36e9.sparta_01eb198736 import qube_b4f373976b
from project.sparta_c2313b36e9.sparta_60a9de74f2 import qube_041ae60ad3
def get_url_patterns():l='deleteMember';k='giveAdminRights';j='leaveGroup';i='deleteGroup';h='loadGroupMembers';g='updateGroup';f='loadGroups';e='createGroup';d='helpCenterGetNumberNotification';c='helpCenterSendMessage';b='helpCenterClose';a='helpCenterLoadConversation';Z='helpCenterLoad';Y='helpCenterCreate';X='settingsContactUs';W='updateImageProfile';V='updatePassword';U='changeDarkTheme';T='codeEditorTheme';S='network_master_reset_password';R='token_reset_password_worker';Q='update_spartaqube_code';P='reset_password';O='setSeenNotification';N='loadNotifications';M='help-center-notification';L='help-center';K='settings-profile';J='home';I='notLoggerAPI';H='banned';G='reset-password-change';F='reset-password';E='logout';D='registration-pending';C='registration';B='login';A='registration-validation';return[path('admin/',admin.site.urls),path('',qube_cde64080a5.sparta_38fb67a5f2,name='baseUri'),path(B,qube_cde64080a5.sparta_38fb67a5f2,name=B),path('login/<str:redirectUrl>',qube_cde64080a5.sparta_ede5fc3e3e,name='loginRedirect'),path(C,qube_cde64080a5.sparta_66326ed2de,name=C),path(D,qube_cde64080a5.sparta_9a7643373a,name=D),path(A,qube_cde64080a5.sparta_b9d5630552,name=A),path('registration-validation/<str:token>',qube_cde64080a5.sparta_b9d5630552,name=A),path(E,qube_cde64080a5.sparta_2dbe5ab0ce,name=E),path(F,qube_cde64080a5.sparta_78cad2043d,name=F),path(G,qube_cde64080a5.sparta_f0a4a2b1f0,name=G),path(H,qube_cde64080a5.sparta_dd95f302cf,name=H),path(I,qube_cde64080a5.sparta_0db1c9107d,name=I),path(J,qube_9ab238a798.sparta_0d3277309e,name=J),path(K,qube_6c85283e81.sparta_9fb8d561e4,name=K),path('settings-profile/<int:idSection>',qube_6c85283e81.sparta_9fb8d561e4,name='settings-profile-params'),path(L,qube_30d3f5b738.sparta_1d7bc516b7,name=L),path(M,qube_30d3f5b738.sparta_5738fd34a5,name=M),path(N,qube_11486cd76c.sparta_cec50689f4,name=N),path(O,qube_11486cd76c.sparta_001b3db896,name=O),path(P,qube_1f4b0baf84.sparta_b1d9c860ca,name=P),path(Q,qube_1f4b0baf84.sparta_ff67c82dc1,name=Q),path(R,qube_1f4b0baf84.sparta_b636ccac7b,name=R),path(S,qube_1f4b0baf84.sparta_2fb414b856,name=S),path(T,qube_1f4b0baf84.sparta_d48337e863,name=T),path(U,qube_1f4b0baf84.sparta_bb3fa38a91,name=U),path(V,qube_1f4b0baf84.sparta_950b84d70a,name=V),path(W,qube_1f4b0baf84.sparta_6e01ceba7d,name=W),path(X,qube_1f4b0baf84.sparta_1b85c2733c,name=X),path(Y,qube_b4f373976b.sparta_80ee476f5a,name=Y),path(Z,qube_b4f373976b.sparta_2f38f4f00f,name=Z),path(a,qube_b4f373976b.sparta_bdfd9b349f,name=a),path(b,qube_b4f373976b.sparta_811573dfb6,name=b),path(c,qube_b4f373976b.sparta_8d7f39425e,name=c),path(d,qube_b4f373976b.sparta_d02bdca957,name=d),path(e,qube_041ae60ad3.sparta_241a35df77,name=e),path(f,qube_041ae60ad3.sparta_f0e9ac630f,name=f),path(g,qube_041ae60ad3.sparta_39b764d86a,name=g),path(h,qube_041ae60ad3.sparta_4b33f9efc8,name=h),path(i,qube_041ae60ad3.sparta_7204d7a68e,name=i),path(j,qube_041ae60ad3.sparta_7dfcf3974e,name=j),path(k,qube_041ae60ad3.sparta_a40ed1f7b9,name=k),path(l,qube_041ae60ad3.sparta_b6def299fb,name=l)]