FROM nginx:1.15.8

ADD fruit.json /usr/share/nginx/html/fruit.json
ADD nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]