FROM node AS build

WORKDIR /project
COPY package.json yarn.lock ./

RUN yarn install
COPY . .
RUN yarn build

FROM nginx:stable-alpine
COPY --from=build /project/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
