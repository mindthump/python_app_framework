#!/usr/bin/env bash

echo "Outside the Cluster:"
http 10.0.0.10:30088/fruit

echo "On a Node:"
http localhost:8088/fruit
