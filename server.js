const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 5000;

const MIME_TYPES = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.ico': 'image/x-icon'
};

function getMimeType(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    return MIME_TYPES[ext] || 'application/octet-stream';
}

function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
    res.end(JSON.stringify(data));
}

function sendFile(res, filePath) {
    const mimeType = getMimeType(filePath);
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('File not found');
            return;
        }
        res.writeHead(200, { 'Content-Type': mimeType });
        res.end(data);
    });
}

const allMatches = [
    { id: 1, group_name: 'A', stage: '小组赛', home_team: '墨西哥', away_team: '南非', home_score: '', away_score: '', match_date: '2026-06-12', match_time: '03:00', venue: '墨西哥城球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 2, group_name: 'A', stage: '小组赛', home_team: '韩国', away_team: '捷克', home_score: '', away_score: '', match_date: '2026-06-12', match_time: '10:00', venue: '瓜达拉哈拉球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 3, group_name: 'B', stage: '小组赛', home_team: '加拿大', away_team: '波黑', home_score: '', away_score: '', match_date: '2026-06-13', match_time: '03:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 4, group_name: 'D', stage: '小组赛', home_team: '美国', away_team: '巴拉圭', home_score: '', away_score: '', match_date: '2026-06-13', match_time: '09:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 5, group_name: 'C', stage: '小组赛', home_team: '海地', away_team: '苏格兰', home_score: '', away_score: '', match_date: '2026-06-14', match_time: '09:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 6, group_name: 'D', stage: '小组赛', home_team: '澳大利亚', away_team: '土耳其', home_score: '', away_score: '', match_date: '2026-06-14', match_time: '12:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 7, group_name: 'C', stage: '小组赛', home_team: '巴西', away_team: '摩洛哥', home_score: '', away_score: '', match_date: '2026-06-14', match_time: '06:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 8, group_name: 'B', stage: '小组赛', home_team: '卡塔尔', away_team: '瑞士', home_score: '', away_score: '', match_date: '2026-06-14', match_time: '03:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 9, group_name: 'E', stage: '小组赛', home_team: '科特迪瓦', away_team: '厄瓜多尔', home_score: '', away_score: '', match_date: '2026-06-15', match_time: '07:00', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 10, group_name: 'E', stage: '小组赛', home_team: '德国', away_team: '库拉索', home_score: '', away_score: '', match_date: '2026-06-15', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 11, group_name: 'F', stage: '小组赛', home_team: '荷兰', away_team: '日本', home_score: '', away_score: '', match_date: '2026-06-15', match_time: '04:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 12, group_name: 'F', stage: '小组赛', home_team: '瑞典', away_team: '突尼斯', home_score: '', away_score: '', match_date: '2026-06-15', match_time: '10:00', venue: '蒙特雷球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 13, group_name: 'H', stage: '小组赛', home_team: '沙特阿拉伯', away_team: '乌拉圭', home_score: '', away_score: '', match_date: '2026-06-16', match_time: '06:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 14, group_name: 'H', stage: '小组赛', home_team: '西班牙', away_team: '佛得角', home_score: '', away_score: '', match_date: '2026-06-16', match_time: '00:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 15, group_name: 'G', stage: '小组赛', home_team: '伊朗', away_team: '新西兰', home_score: '', away_score: '', match_date: '2026-06-16', match_time: '09:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 16, group_name: 'G', stage: '小组赛', home_team: '比利时', away_team: '埃及', home_score: '', away_score: '', match_date: '2026-06-16', match_time: '03:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 17, group_name: 'I', stage: '小组赛', home_team: '法国', away_team: '塞内加尔', home_score: '', away_score: '', match_date: '2026-06-17', match_time: '03:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 18, group_name: 'I', stage: '小组赛', home_team: '伊拉克', away_team: '挪威', home_score: '', away_score: '', match_date: '2026-06-17', match_time: '06:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 19, group_name: 'J', stage: '小组赛', home_team: '阿根廷', away_team: '阿尔及利亚', home_score: '', away_score: '', match_date: '2026-06-17', match_time: '09:00', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 20, group_name: 'J', stage: '小组赛', home_team: '奥地利', away_team: '约旦', home_score: '', away_score: '', match_date: '2026-06-17', match_time: '12:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 21, group_name: 'L', stage: '小组赛', home_team: '加纳', away_team: '巴拿马', home_score: '', away_score: '', match_date: '2026-06-18', match_time: '07:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 22, group_name: 'L', stage: '小组赛', home_team: '英格兰', away_team: '克罗地亚', home_score: '', away_score: '', match_date: '2026-06-18', match_time: '04:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 23, group_name: 'K', stage: '小组赛', home_team: '葡萄牙', away_team: '民主刚果', home_score: '', away_score: '', match_date: '2026-06-18', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 24, group_name: 'K', stage: '小组赛', home_team: '乌兹别克斯坦', away_team: '哥伦比亚', home_score: '', away_score: '', match_date: '2026-06-18', match_time: '10:00', venue: '墨西哥城球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 25, group_name: 'A', stage: '小组赛', home_team: '捷克', away_team: '南非', home_score: '', away_score: '', match_date: '2026-06-19', match_time: '00:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 26, group_name: 'B', stage: '小组赛', home_team: '瑞士', away_team: '波黑', home_score: '', away_score: '', match_date: '2026-06-19', match_time: '03:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 27, group_name: 'B', stage: '小组赛', home_team: '加拿大', away_team: '卡塔尔', home_score: '', away_score: '', match_date: '2026-06-19', match_time: '06:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 28, group_name: 'A', stage: '小组赛', home_team: '墨西哥', away_team: '韩国', home_score: '', away_score: '', match_date: '2026-06-19', match_time: '09:00', venue: '瓜达拉哈拉球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 29, group_name: 'C', stage: '小组赛', home_team: '巴西', away_team: '海地', home_score: '', away_score: '', match_date: '2026-06-20', match_time: '08:30', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 30, group_name: 'C', stage: '小组赛', home_team: '苏格兰', away_team: '摩洛哥', home_score: '', away_score: '', match_date: '2026-06-20', match_time: '06:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 31, group_name: 'D', stage: '小组赛', home_team: '土耳其', away_team: '巴拉圭', home_score: '', away_score: '', match_date: '2026-06-20', match_time: '11:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 32, group_name: 'D', stage: '小组赛', home_team: '美国', away_team: '澳大利亚', home_score: '', away_score: '', match_date: '2026-06-20', match_time: '03:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 33, group_name: 'E', stage: '小组赛', home_team: '德国', away_team: '科特迪瓦', home_score: '', away_score: '', match_date: '2026-06-21', match_time: '04:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 34, group_name: 'E', stage: '小组赛', home_team: '厄瓜多尔', away_team: '库拉索', home_score: '', away_score: '', match_date: '2026-06-21', match_time: '08:00', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 35, group_name: 'F', stage: '小组赛', home_team: '荷兰', away_team: '瑞典', home_score: '', away_score: '', match_date: '2026-06-21', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 36, group_name: 'F', stage: '小组赛', home_team: '突尼斯', away_team: '日本', home_score: '', away_score: '', match_date: '2026-06-21', match_time: '12:00', venue: '蒙特雷球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 37, group_name: 'H', stage: '小组赛', home_team: '乌拉圭', away_team: '佛得角', home_score: '', away_score: '', match_date: '2026-06-22', match_time: '06:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 38, group_name: 'H', stage: '小组赛', home_team: '西班牙', away_team: '沙特阿拉伯', home_score: '', away_score: '', match_date: '2026-06-22', match_time: '00:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 39, group_name: 'G', stage: '小组赛', home_team: '比利时', away_team: '伊朗', home_score: '', away_score: '', match_date: '2026-06-22', match_time: '03:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 40, group_name: 'G', stage: '小组赛', home_team: '新西兰', away_team: '埃及', home_score: '', away_score: '', match_date: '2026-06-22', match_time: '09:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 41, group_name: 'I', stage: '小组赛', home_team: '挪威', away_team: '塞内加尔', home_score: '', away_score: '', match_date: '2026-06-23', match_time: '08:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 42, group_name: 'I', stage: '小组赛', home_team: '法国', away_team: '伊拉克', home_score: '', away_score: '', match_date: '2026-06-23', match_time: '05:00', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 43, group_name: 'J', stage: '小组赛', home_team: '阿根廷', away_team: '奥地利', home_score: '', away_score: '', match_date: '2026-06-23', match_time: '01:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 44, group_name: 'J', stage: '小组赛', home_team: '约旦', away_team: '阿尔及利亚', home_score: '', away_score: '', match_date: '2026-06-23', match_time: '11:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 45, group_name: 'L', stage: '小组赛', home_team: '英格兰', away_team: '加纳', home_score: '', away_score: '', match_date: '2026-06-24', match_time: '04:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 46, group_name: 'L', stage: '小组赛', home_team: '巴拿马', away_team: '克罗地亚', home_score: '', away_score: '', match_date: '2026-06-24', match_time: '07:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 47, group_name: 'K', stage: '小组赛', home_team: '葡萄牙', away_team: '乌兹别克斯坦', home_score: '', away_score: '', match_date: '2026-06-24', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 48, group_name: 'K', stage: '小组赛', home_team: '哥伦比亚', away_team: '民主刚果', home_score: '', away_score: '', match_date: '2026-06-24', match_time: '10:00', venue: '瓜达拉哈拉球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 49, group_name: 'C', stage: '小组赛', home_team: '苏格兰', away_team: '巴西', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '06:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 50, group_name: 'C', stage: '小组赛', home_team: '摩洛哥', away_team: '海地', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '06:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 51, group_name: 'B', stage: '小组赛', home_team: '瑞士', away_team: '加拿大', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '03:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 52, group_name: 'B', stage: '小组赛', home_team: '波黑', away_team: '卡塔尔', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '03:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 53, group_name: 'A', stage: '小组赛', home_team: '捷克', away_team: '墨西哥', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '09:00', venue: '墨西哥城球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 54, group_name: 'A', stage: '小组赛', home_team: '南非', away_team: '韩国', home_score: '', away_score: '', match_date: '2026-06-25', match_time: '09:00', venue: '蒙特雷球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 55, group_name: 'E', stage: '小组赛', home_team: '库拉索', away_team: '科特迪瓦', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '04:00', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 56, group_name: 'E', stage: '小组赛', home_team: '厄瓜多尔', away_team: '德国', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '04:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 57, group_name: 'F', stage: '小组赛', home_team: '日本', away_team: '瑞典', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '07:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 58, group_name: 'F', stage: '小组赛', home_team: '突尼斯', away_team: '荷兰', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '07:00', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 59, group_name: 'D', stage: '小组赛', home_team: '土耳其', away_team: '美国', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '10:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 60, group_name: 'D', stage: '小组赛', home_team: '巴拉圭', away_team: '澳大利亚', home_score: '', away_score: '', match_date: '2026-06-26', match_time: '10:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 61, group_name: 'I', stage: '小组赛', home_team: '挪威', away_team: '法国', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '03:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 62, group_name: 'I', stage: '小组赛', home_team: '塞内加尔', away_team: '伊拉克', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '03:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 63, group_name: 'G', stage: '小组赛', home_team: '埃及', away_team: '伊朗', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '11:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 64, group_name: 'G', stage: '小组赛', home_team: '新西兰', away_team: '比利时', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '11:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 65, group_name: 'H', stage: '小组赛', home_team: '佛得角', away_team: '沙特阿拉伯', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '08:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 66, group_name: 'H', stage: '小组赛', home_team: '乌拉圭', away_team: '西班牙', home_score: '', away_score: '', match_date: '2026-06-27', match_time: '08:00', venue: '瓜达拉哈拉球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 67, group_name: 'L', stage: '小组赛', home_team: '巴拿马', away_team: '英格兰', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '05:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 68, group_name: 'L', stage: '小组赛', home_team: '克罗地亚', away_team: '加纳', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '05:00', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 69, group_name: 'J', stage: '小组赛', home_team: '阿尔及利亚', away_team: '奥地利', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '10:00', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 70, group_name: 'J', stage: '小组赛', home_team: '约旦', away_team: '阿根廷', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '10:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 71, group_name: 'K', stage: '小组赛', home_team: '哥伦比亚', away_team: '葡萄牙', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '07:30', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 72, group_name: 'K', stage: '小组赛', home_team: '民主刚果', away_team: '乌兹别克斯坦', home_score: '', away_score: '', match_date: '2026-06-28', match_time: '07:30', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 73, group_name: '', stage: '1/16决赛', home_team: 'A2', away_team: 'B2', home_score: '', away_score: '', match_date: '2026-06-29', match_time: '03:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 74, group_name: '', stage: '1/16决赛', home_team: 'E1', away_team: 'A/B/C/D/F3', home_score: '', away_score: '', match_date: '2026-06-30', match_time: '04:30', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 75, group_name: '', stage: '1/16决赛', home_team: 'F1', away_team: 'C2', home_score: '', away_score: '', match_date: '2026-06-30', match_time: '09:00', venue: '蒙特雷体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 76, group_name: '', stage: '1/16决赛', home_team: 'C1', away_team: 'F2', home_score: '', away_score: '', match_date: '2026-06-30', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 77, group_name: '', stage: '1/16决赛', home_team: 'I1', away_team: 'C/D/F/G/H3', home_score: '', away_score: '', match_date: '2026-07-01', match_time: '05:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 78, group_name: '', stage: '1/16决赛', home_team: 'E2', away_team: 'I2', home_score: '', away_score: '', match_date: '2026-07-01', match_time: '01:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 79, group_name: '', stage: '1/16决赛', home_team: 'A1', away_team: 'C/E/F/H/I3', home_score: '', away_score: '', match_date: '2026-07-01', match_time: '09:00', venue: '墨西哥城球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 80, group_name: '', stage: '1/16决赛', home_team: 'L1', away_team: 'E/H/I/J/K3', home_score: '', away_score: '', match_date: '2026-07-02', match_time: '00:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 81, group_name: '', stage: '1/16决赛', home_team: 'D1', away_team: 'B/E/F/I/J3', home_score: '', away_score: '', match_date: '2026-07-02', match_time: '08:00', venue: '旧金山湾区体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 82, group_name: '', stage: '1/16决赛', home_team: 'G1', away_team: 'A/E/H/I/J3', home_score: '', away_score: '', match_date: '2026-07-02', match_time: '04:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 83, group_name: '', stage: '1/16决赛', home_team: 'K2', away_team: 'L2', home_score: '', away_score: '', match_date: '2026-07-03', match_time: '07:00', venue: '多伦多体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 84, group_name: '', stage: '1/16决赛', home_team: 'H1', away_team: 'J2', home_score: '', away_score: '', match_date: '2026-07-03', match_time: '03:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 85, group_name: '', stage: '1/16决赛', home_team: 'B1', away_team: 'E/F/G/I/J3', home_score: '', away_score: '', match_date: '2026-07-03', match_time: '11:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 86, group_name: '', stage: '1/16决赛', home_team: 'J1', away_team: 'H2', home_score: '', away_score: '', match_date: '2026-07-04', match_time: '06:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 87, group_name: '', stage: '1/16决赛', home_team: 'K1', away_team: 'D/E/I/J/L3', home_score: '', away_score: '', match_date: '2026-07-04', match_time: '09:30', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 88, group_name: '', stage: '1/16决赛', home_team: 'D2', away_team: 'G2', home_score: '', away_score: '', match_date: '2026-07-04', match_time: '02:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 89, group_name: '', stage: '1/8决赛', home_team: '74胜者', away_team: '77胜者', home_score: '', away_score: '', match_date: '2026-07-05', match_time: '05:00', venue: '费城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 90, group_name: '', stage: '1/8决赛', home_team: '73胜者', away_team: '75胜者', home_score: '', away_score: '', match_date: '2026-07-05', match_time: '01:00', venue: '休斯敦体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 91, group_name: '', stage: '1/8决赛', home_team: '76胜者', away_team: '78胜者', home_score: '', away_score: '', match_date: '2026-07-06', match_time: '04:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 92, group_name: '', stage: '1/8决赛', home_team: '79胜者', away_team: '80胜者', home_score: '', away_score: '', match_date: '2026-07-06', match_time: '08:00', venue: '墨西哥城球场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 93, group_name: '', stage: '1/8决赛', home_team: '83胜者', away_team: '84胜者', home_score: '', away_score: '', match_date: '2026-07-07', match_time: '03:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 94, group_name: '', stage: '1/8决赛', home_team: '81胜者', away_team: '82胜者', home_score: '', away_score: '', match_date: '2026-07-07', match_time: '08:00', venue: '西雅图体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 95, group_name: '', stage: '1/8决赛', home_team: '86胜者', away_team: '88胜者', home_score: '', away_score: '', match_date: '2026-07-08', match_time: '00:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 96, group_name: '', stage: '1/8决赛', home_team: '85胜者', away_team: '87胜者', home_score: '', away_score: '', match_date: '2026-07-08', match_time: '04:00', venue: '温哥华体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 97, group_name: '', stage: '1/4决赛', home_team: '89胜者', away_team: '90胜者', home_score: '', away_score: '', match_date: '2026-07-10', match_time: '04:00', venue: '波士顿体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 98, group_name: '', stage: '1/4决赛', home_team: '93胜者', away_team: '94胜者', home_score: '', away_score: '', match_date: '2026-07-11', match_time: '03:00', venue: '洛杉矶体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 99, group_name: '', stage: '1/4决赛', home_team: '91胜者', away_team: '92胜者', home_score: '', away_score: '', match_date: '2026-07-12', match_time: '05:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 100, group_name: '', stage: '1/4决赛', home_team: '95胜者', away_team: '96胜者', home_score: '', away_score: '', match_date: '2026-07-12', match_time: '09:00', venue: '堪萨斯城体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 101, group_name: '', stage: '半决赛', home_team: '97胜者', away_team: '100胜者', home_score: '', away_score: '', match_date: '2026-07-15', match_time: '03:00', venue: '达拉斯体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 102, group_name: '', stage: '半决赛', home_team: '98胜者', away_team: '99胜者', home_score: '', away_score: '', match_date: '2026-07-16', match_time: '03:00', venue: '亚特兰大体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 103, group_name: '', stage: '季军战', home_team: '101负者', away_team: '102负者', home_score: '', away_score: '', match_date: '2026-07-19', match_time: '05:00', venue: '迈阿密体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 },
    { id: 104, group_name: '', stage: '决赛', home_team: '101胜者', away_team: '102胜者', home_score: '', away_score: '', match_date: '2026-07-20', match_time: '03:00', venue: '纽约新泽西体育场', home_yellow_card: 0, home_red_card: 0, away_yellow_card: 0, away_red_card: 0 }
];

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    if (req.method === 'OPTIONS') {
        res.writeHead(200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        });
        res.end();
        return;
    }

    if (pathname === '/api/matches') {
        if (req.method === 'GET') {
            const year = parsedUrl.query.year || '2026';
            const filteredMatches = allMatches.filter(m => m.match_date.startsWith(year));
            sendJSON(res, 200, filteredMatches);
        } else {
            sendJSON(res, 405, { error: 'Method not allowed' });
        }
        return;
    }

    if (pathname.startsWith('/api/matches/') && req.method === 'PUT') {
        const id = parseInt(pathname.split('/')[3]);
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const match = allMatches.find(m => m.id === id);
                if (match) {
                    match.home_score = data.home_score || '';
                    match.away_score = data.away_score || '';
                    match.home_yellow_card = data.home_yellow_card || 0;
                    match.home_red_card = data.home_red_card || 0;
                    match.away_yellow_card = data.away_yellow_card || 0;
                    match.away_red_card = data.away_red_card || 0;
                    sendJSON(res, 200, { success: true, updated_match: match });
                } else {
                    sendJSON(res, 404, { error: 'Match not found' });
                }
            } catch (err) {
                sendJSON(res, 400, { error: 'Invalid JSON' });
            }
        });
        return;
    }

    if (pathname === '/') {
        sendFile(res, path.join(__dirname, 'index.html'));
        return;
    }

    const filePath = path.join(__dirname, pathname);
    if (fs.existsSync(filePath)) {
        sendFile(res, filePath);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log('');
    console.log('\x1b[32m========================================\x1b[0m');
    console.log('\x1b[32m  2026 世界杯数据中心\x1b[0m');
    console.log('\x1b[32m========================================\x1b[0m');
    console.log('');
    console.log('\x1b[36m  Server running at http://localhost:' + PORT + '\x1b[0m');
    console.log('\x1b[36m  Open in browser: http://localhost:' + PORT + '\x1b[0m');
    console.log('');
    console.log('\x1b[33m  Total matches: ' + allMatches.length + ' (including all group stage & knockout)\x1b[0m');
    console.log('');
});