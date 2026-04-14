"""
╔══════════════════════════════════════════════════════════════════╗
║          CU SMART ASSISTANT — SINGLE FILE EDITION               ║
║                                                                  ║
║  Share just THIS file. No templates/, no .json, no .env needed. ║
║                                                                  ║
║  SETUP (one time only):                                          ║
║    pip install flask google-generativeai python-dotenv           ║
║                                                                  ║
║  RUN:                                                            ║
║    python CU_Smart_Assistant_SINGLE_FILE.py                      ║
║                                                                  ║
║  Then open:  http://127.0.0.1:5000                               ║
║                                                                  ║
║  API KEY (optional — works offline without one):                 ║
║    Set env variable:  GOOGLE_API_KEY=your_key_here               ║
║    Or create a .env file next to this script with that line.     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# ──────────────────────────────────────────────────────────────────
# EMBEDDED FACULTY DATABASE
# ──────────────────────────────────────────────────────────────────
FACULTY_DATA = [
  {"institute":"UID","program":"Fashion Design","name":"Dr. Pooja Bhatt","email":"pooja.e12218@cumail.in","phone":"7579130236","room":"812","block":"A3"},
  {"institute":"UID","program":"B.Des, B.Sc","name":"Manpreet Singh","email":"manpreetsingh.e9333@cumail.in","phone":"9915365037","room":"712","block":"A3"},
  {"institute":"UID","program":"B Fine Arts","name":"Ms. Sarvpriya Kaur","email":"sarvpriya.e15572@cumail.in","phone":"7009468984","room":"810","block":"A3"},
  {"institute":"UILAH","program":"Liberal Arts & English","name":"Ms. Manvi Khosla","email":"Manvi.e14125@cumail.in","phone":"8988938480","room":"413","block":"A3"},
  {"institute":"UILAH","program":"Liberal Arts (B.A. Psychology (Hons))","name":"Shilpa Singh Rohilla","email":"shilpa.e19043@cumail.in","phone":"6283173103","room":"511","block":"A3"},
  {"institute":"UIFVA-Animation","program":"B.Sc Animation, VFX and Gaming","name":"Mr. Ramandeep Sharma","email":"ramandeep.e8879@cumail.in","phone":"9082770064","room":"707-A","block":"A2"},
  {"institute":"UIAHS/UIN","program":"Health & Allied Sciences","name":"Ms. Karpreet Sharma","email":"karpreet.e14046@cumail.in","phone":"9780730167","room":"501","block":"D8"},
  {"institute":"UITTR","program":"BA.BEd., B.Sc.BEd.","name":"Dr. Ranjeeta Saini","email":"ranjeeta.e15460@cumail.in","phone":"9813204902","room":"513","block":"A3"},
  {"institute":"UIMS","program":"BAJMC","name":"Dr. Gurpreet Kaur","email":"gurpreet.e15391@cumail.in","phone":"9803616268","room":"614","block":"A2"},
  {"institute":"UIA","program":"B.ARCH","name":"Sheril Chugh","email":"sheril.e9660@cumail.in","phone":"8689084788","room":"305","block":"A2"},
  {"institute":"UID","program":"Industrial Design","name":"Mr. Rishabh Chowdhury","email":"rishabh.e19064@cumail.in","phone":"9129213151","room":"711","block":"A3"},
  {"institute":"UITHM DOT","program":"BSc.TTM","name":"Dr. Trilochan","email":"trilochan.e15928@cumail.in","phone":"8700089833","room":"715","block":"B2"},
  {"institute":"UITHM","program":"B.Sc. AAM","name":"Ms Ishpreet Kaur","email":"ishpreet.e15465@cumail.in","phone":"9082700060","room":"615","block":"B2"},
  {"institute":"UITHM DOH","program":"B.Sc. HHA","name":"Kanwardeep Singh Sokhi","email":"kanwardeep.e17667@cumail.in","phone":"8528555486","room":"515","block":"B2"},
  {"institute":"UITHM DOH","program":"B.Sc. Culinary Science","name":"Kanwardeep Singh Sokhi","email":"kanwardeep.e17667@cumail.in","phone":"8528555486","room":"515","block":"B2"},
  {"institute":"USB","program":"BBA","name":"Dampy Singh","email":"dampy.e19208@cumail.in","phone":"9927716342","room":"116","block":"DD3"},
  {"institute":"USB","program":"BBA","name":"Dr. Anil Chandok","email":"anil.e4863@cumail.in","phone":"9416295795","room":"221","block":"DD3"},
  {"institute":"USB","program":"BBA","name":"Dr. Meenakshi","email":"meenakshi.usb@cumail.in","phone":"9780244684","room":"412","block":"DD3"},
  {"institute":"USB","program":"BBA","name":"Dr. Kritika Gupta","email":"kritika.e7094@cumail.in","phone":"8708624583","room":"121","block":"DD3"},
  {"institute":"USB","program":"Commerce","name":"Ambu Sharma","email":"ambu.e13140@cumail.in","phone":"9456200999","room":"112","block":"DD5"},
  {"institute":"USB","program":"BBA APEX","name":"Ms. Saroj Rani","email":"saroj.e3928@cumail.in","phone":"8053743238","room":"507","block":"D8"},
  {"institute":"USB","program":"MBA-APEX","name":"Dr. Anju Bala","email":"anju.e16263@cumail.in","phone":"7837176100","room":"502","block":"D1"},
  {"institute":"USB","program":"MBA","name":"Dr. Anjali Vyas","email":"ANJALI.E12890@CUMAIL.IN","phone":"9829861675","room":"206","block":"D5"},
  {"institute":"USB","program":"Economics","name":"Ms. Silky Valecha","email":"SILKY.E13006@CUMAIL.IN","phone":"8872863204","room":"406","block":"D5"},
  {"institute":"GSFA","program":"Bcom with ACCA / MBA in Applied Finance / BBA with ACCA","name":"Ms. Prabh Simran Kaur","email":"prabhsimran.e19388@cumail.in","phone":"8288838778","room":"603","block":"D8"},
  {"institute":"UIAHS","program":"Bachelor of Physiotherapy","name":"Dr. Taniya Wadhwa","email":"taniya.e9885@cumail.in","phone":"7015728068","room":"506","block":"D7"},
  {"institute":"UIAHS","program":"BSc Forensic Science","name":"Ms. Amanpreet Kaur","email":"amanpreet.e5622@cumail.in","phone":"7087499453","room":"306","block":"D7"},
  {"institute":"UIAHS","program":"Nutrition & Dietetics","name":"Dr. Jyoti Rani","email":"jyoti.e8920@cumail.in","phone":"9463753513","room":"224","block":"D7"},
  {"institute":"UIAHS","program":"Medical Lab Technology (MLT)","name":"Syed Yunis Bukhari","email":"yunis.e16472@cumail.in","phone":"7006377239","room":"204","block":"D7"},
  {"institute":"UIAHS","program":"Bachelor of Optometry","name":"Iqra Jamaal Khan","email":"Iqura.e15679@cumail.in","phone":"8081879196","room":"214","block":"D7"},
  {"institute":"UIBT","program":"BSc Biotechnology / BSc Microbiology","name":"Dr. Namrata Gupta","email":"namrata.e12238@cumail.in","phone":"9450147477","room":"716A","block":"A1"},
  {"institute":"UIBT","program":"BSc Biotechnology / BSc Microbiology","name":"Dr. Anil Kumar","email":"anil.e8226@cumail.in","phone":"9459011110","room":"306","block":"A1"},
  {"institute":"UIBT-Biosciences","program":"B.Sc Medical","name":"Dr. Shailika Sharma","email":"shailika.e15666@cumail.in","phone":"7018048154","room":"424","block":"A1"},
  {"institute":"UIS","program":"Mathematics","name":"Dr. Vikas Garg","email":"vikas.e9995@cumail.in","phone":"9999982004","room":"309","block":"DD1"},
  {"institute":"UIS","program":"Physics","name":"Dr. Shilpi Jindal","email":"shilpi.e2941@cumail.in","phone":"9988320437","room":"102","block":"DD2"},
  {"institute":"UIS","program":"Chemistry","name":"Dr. Kanika Guleria","email":"kanika.e19098@cumail.in","phone":"6230777992","room":"406","block":"D7"},
  {"institute":"UILS","program":"LLM","name":"Mr. Omair","email":"omair.e15533@cumail.in","phone":"8709888807","room":"Level 2","block":"B5"},
  {"institute":"UILS","program":"BBA.LLB (Hons.)","name":"Ms. Doli Arora","email":"Doli.e11408@cumail.in","phone":"9649200162","room":"Level 3","block":"B5"},
  {"institute":"UILS","program":"BCOMLLB (Hons.)","name":"Prof. (Dr) Nitin Gupta","email":"nitin.e11888@cumail.in","phone":"9997303920","room":"Level 4","block":"B5"},
  {"institute":"UILS","program":"B.A.LL.B (Hons.)","name":"Dr. Ishan Khan","email":"ishan.e16583@cumail.in","phone":"9837412566","room":"Level 4","block":"B5"},
  {"institute":"UILS","program":"B.A.LL.B (Hons.)","name":"Ms. Priyanka Thakur","email":"priyanka.e14372@cumail.in","phone":"7876839225","room":"Level 4","block":"B5"},
  {"institute":"UILS","program":"B.A.LL.B (Hons.)","name":"Dr. Manpreet Kaur","email":"manpreet.e13358@cumail.in","phone":"9914408910","room":"Level 2","block":"B5"},
  {"institute":"UIE","program":"Mechanical Engineering","name":"Dr. Suman Debnath","email":"suman.e11804@cumail.in","phone":"7719715500","room":"202","block":"B4"},
  {"institute":"UIE","program":"Mechatronics","name":"Dr. Inderpreet Singh","email":"inderpreet.e1468@cumail.in","phone":"9041615108","room":"312","block":"B4"},
  {"institute":"UIE","program":"Chemical Engineering","name":"Dr. Vikas Kumar Chaudhary","email":"vikas.e13477@cumail.in","phone":"7275816697","room":"412","block":"B4"},
  {"institute":"UIE","program":"Civil Engineering","name":"Dr. Mohit Bhandari","email":"mohit.e8967@cumail.in","phone":"9814780422","room":"612","block":"B4"},
  {"institute":"UIE","program":"Aerospace Engineering","name":"Dr. Ajin Branesh Asokan","email":"ajin.e8705@cumail.in","phone":"7548898308","room":"NA","block":"B4"},
  {"institute":"UIE","program":"Automobile Engineering","name":"Dr. Bikramjeet Singh","email":"bikramjeet.e4150@cumail.in","phone":"9464496800","room":"312","block":"B4"},
  {"institute":"UIE","program":"Biotech Engineering","name":"Dr. Dinesh Bhardwaj","email":"dinesh.e15022@cumail.in","phone":"8570944885","room":"510","block":"B4"},
  {"institute":"AIT CSE","program":"AIML","name":"Ms. Tanvi","email":"tanvi.e15506@cumail.in","phone":"9914171477","room":"313","block":"D2"},
  {"institute":"AIT CSE","program":"AIML","name":"Ms. Mamta Punia","email":"mamta.e12337@cumail.in","phone":"9988039708","room":"313","block":"D2"},
  {"institute":"AIT CSE","program":"Cloud / DevOps / FullStack / Security / Data Science / IoT / Blockchain","name":"Savita","email":"savita.uie@cumail.in","phone":"9914141254","room":"310","block":"D3"},
  {"institute":"AIT CSE","program":"Cloud / DevOps / FullStack / Security / Data Science / IoT / Blockchain","name":"Mr. Abhishek Tiwari","email":"abhishek.e15792@cumail.in","phone":"9827605090","room":"206","block":"D3"},
  {"institute":"UIE Foundation","program":"CSE (AIML, Cyber Security, Data Science, IoT, Cloud, Full Stack, TCS)","name":"Tushar Verma","email":"tushar.E11817@cumail.in","phone":"7206733916","room":"302","block":"C1"},
  {"institute":"UIE Foundation","program":"B.E. Computer Science & Engineering","name":"Nishu Bansal","email":"nishubansal.cse@cumail.in","phone":"8146550163","room":"113","block":"C3"},
  {"institute":"UIE Foundation","program":"General CSE / AIML","name":"Charanpreet Kaur","email":"Charanpreete6227@cumail.in","phone":"9815926889","room":"610","block":"C1"},
  {"institute":"UIE Foundation","program":"BE CSE","name":"Er. Rohit Katyal","email":"Rohit.cse@cumail.in","phone":"7707876820","room":"711-A","block":"C3"},
  {"institute":"UIE-PG","program":"ME.CSE, ME.CSE(AIML), ME(AI), ME CSE(CC), ME CSE(DS)","name":"Paurav Goel","email":"paurav.e14409@cumail.in","phone":"9315866060","room":"401-A","block":"B1"},
  {"institute":"UIC","program":"BCA / BCA(UI UX) / BCA(DS) / BCA(CS) / BCA(ITP)","name":"Ms. Riya Mondal","email":"riya.e17321@cumail.in","phone":"7003611282","room":"North Campus","block":"E2"},
  {"institute":"UIC","program":"BCA / BCA(UI UX) / BCA(DS) / BCA(CS) / BCA(ITP)","name":"Mr. Anup Kumar Singh","email":"Prabhat.e19025@cumail.in","phone":"9593630563","room":"217","block":"E2"},
  {"institute":"UIC","program":"MCA / MCA(ITP) / MCA(DS) / MCA(AIML) / MCA(CCD)","name":"Dr. Deeksha Baweja","email":"deeksha.e12115@cumail.in","phone":"8283904606","room":"North Campus","block":"E1"},
  {"institute":"UIC","program":"MCA / MCA(ITP) / MCA(DS) / MCA(AIML) / MCA(CCD)","name":"Ms. Reeti Jaswal","email":"reeti.e13367@cumail.in","phone":"7018957228","room":"North Campus","block":"E1"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Amanpreet Kaur","email":"amanpreet.e15674@cumail.in","phone":"8360202056","room":"601","block":"B3"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Sukhvir Kaur","email":"sukhvir.e11791@cumail.in","phone":"9915369906","room":"601","block":"B3"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Kirat","email":"kirat.e12999@cumail.in","phone":"8968768698","room":"601","block":"B3"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Naveen Chander","email":"naveen.e14410@cumail.in","phone":"7018561927","room":"402","block":"C2"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Neetu Bala","email":"neetu.e15382@cumail.in","phone":"8219428089","room":"501","block":"C2"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Dr. Anshu Mehta","email":"anshu.e13356@cumail.in","phone":"9992808800","room":"611","block":"B1"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Gurpreet Kaur","email":"gurpreet.e12272@cumail.in","phone":"9530836270","room":"310","block":"B1"},
  {"institute":"UIE-CSE","program":"B.E. CSE / IT","name":"Er. Sheikh Affan Farooq","email":"Sheikh.e14180@cumail.in","phone":"8493949654","room":"510","block":"B1"},
  {"institute":"UIE Non-CSE","program":"Electronics & Communication","name":"Dr. Rohin Gupta","email":"rohin.e18749@cumail.in","phone":"9815120777","room":"712","block":"B4"},
  {"institute":"UIE Non-CSE","program":"Electrical Engineering","name":"Dr. Ranjit Kumar Bindal","email":"ranjitbindal.eee@cumail.in","phone":"9888013358","room":"723","block":"B4"},
  {"institute":"UIE Foundation","program":"B.E.","name":"Dr. Ruby Priya","email":"ruby.e10411@cumail.in","phone":"7986065101","room":"504","block":"C3"},
  {"institute":"UIPS","program":"Pharmacy","name":"Ms. Divyanshi","email":"divyanshi.e19379@cumail.in","phone":"9816417928","room":"304","block":"D8"}
]

# ──────────────────────────────────────────────────────────────────
# EMBEDDED HTML TEMPLATE
# ──────────────────────────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CU Smart Assistant</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg: #04080f;
  --surface: #080f1c;
  --card: #0c1628;
  --border: #162240;
  --accent: #00e5ff;
  --accent-dim: rgba(0,229,255,0.12);
  --accent2: #ff6b35;
  --green: #00ff9d;
  --text: #dde8f5;
  --muted: #5a7499;
  --font-head: 'Space Mono', monospace;
  --font-body: 'Outfit', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  height: 100vh;
  width: 100vw;
  margin: 0;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
#bgCanvas {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0;
  pointer-events: none;
}
header {
  position: relative;
  z-index: 10;
  padding: 18px 28px;
  display: flex;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid var(--border);
  background: rgba(8,15,28,0.85);
  backdrop-filter: blur(12px);
}
.logo-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--accent), #0077ff);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  box-shadow: 0 0 20px rgba(0,229,255,0.3);
  flex-shrink: 0;
}
.header-text h1 {
  font-family: var(--font-head);
  font-size: 15px;
  color: var(--accent);
  letter-spacing: 0.05em;
}
.header-text p {
  font-size: 12px;
  color: var(--muted);
  margin-top: 1px;
}
.status-dot {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  color: var(--green);
  font-family: var(--font-head);
}
.status-dot::before {
  content: '';
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }
.main {
  position: relative;
  z-index: 10;
  display: flex;
  flex: 1;
  height: calc(100vh - 77px);
  overflow: hidden;
  min-height: 0;
}
.sidebar {
  width: 260px;
  flex-shrink: 0;
  border-right: 1px solid var(--border);
  background: rgba(8,15,28,0.6);
  display: flex;
  flex-direction: column;
  padding: 16px;
  gap: 10px;
  overflow-y: auto;
}
.sidebar-title {
  font-family: var(--font-head);
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 4px 0 8px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 4px;
}
.quick-btn {
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 12.5px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  line-height: 1.4;
}
.quick-btn:hover {
  border-color: var(--accent);
  background: var(--accent-dim);
  color: var(--accent);
  transform: translateX(3px);
}
.quick-btn .q-icon { font-size: 14px; margin-right: 6px; }
.sidebar-section { margin-top: 8px; }
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
  min-height: 0;
}
.messages::-webkit-scrollbar { width: 4px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
.welcome {
  text-align: center;
  padding: 40px 20px;
  animation: fadeUp 0.6s ease both;
}
.welcome-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: inline-block;
  position: relative;
  filter: drop-shadow(0 0 15px rgba(0,119,255,0.4));
  animation: energeticBob 1.5s ease-in-out infinite;
  z-index: 2;
}
.welcome-icon::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 68px; height: 68px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,119,255,0.2) 0%, rgba(0,229,255,0) 70%);
  box-shadow: 0 0 15px rgba(0,229,255,0.5), 0 0 30px rgba(0,119,255,0.3);
  animation: pulseAura 1.2s infinite alternate;
  z-index: -1;
  pointer-events: none;
}
.welcome-icon::before {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 58px; height: 58px;
  transform: translate(-50%, -50%) rotate(0deg);
  border-radius: 50%;
  border: 2px dashed rgba(0,229,255,0.6);
  animation: spinSparks 3s linear infinite;
  z-index: -1;
  pointer-events: none;
}
@keyframes energeticBob {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-4px) rotate(-4deg); filter: drop-shadow(0 0 25px rgba(0,229,255,0.8)); }
  75% { transform: translateY(-2px) rotate(4deg); }
}
@keyframes pulseAura {
  0% { transform: translate(-50%, -50%) scale(0.9); opacity: 0.6; }
  100% { transform: translate(-50%, -50%) scale(1.15); opacity: 1; }
}
@keyframes spinSparks {
  0% { transform: translate(-50%, -50%) rotate(0deg) scale(1); }
  50% { transform: translate(-50%, -50%) rotate(180deg) scale(1.1); }
  100% { transform: translate(-50%, -50%) rotate(360deg) scale(1); }
}
.welcome h2 {
  font-family: var(--font-head);
  font-size: 22px;
  color: var(--accent);
  margin-bottom: 8px;
}
.welcome p {
  color: var(--muted);
  font-size: 14px;
  max-width: 420px;
  margin: 0 auto;
  line-height: 1.6;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.msg {
  display: flex;
  gap: 12px;
  animation: fadeUp 0.3s ease both;
  max-width: 800px;
}
.msg.user { flex-direction: row-reverse; align-self: flex-end; }
.msg-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 2px;
}
.msg.bot .msg-avatar {
  background: linear-gradient(135deg, var(--accent), #0077ff);
  box-shadow: 0 0 12px rgba(0,229,255,0.25);
}
.msg.user .msg-avatar { background: linear-gradient(135deg, var(--accent2), #ff3d88); }
.msg-bubble {
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.65;
  max-width: calc(100% - 50px);
}
.msg.bot { animation: swoopLeft 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) both; }
.msg.user { animation: swoopRight 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) both; }
@keyframes swoopLeft {
  0% { opacity: 0; transform: translateX(-40px) scale(0.9); }
  100% { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes swoopRight {
  0% { opacity: 0; transform: translateX(40px) scale(0.9); }
  100% { opacity: 1; transform: translateX(0) scale(1); }
}
.msg.bot .msg-bubble {
  background: var(--card);
  border: 1px solid var(--border);
  border-top-left-radius: 4px;
  color: var(--text);
}
.msg.user .msg-bubble {
  background: linear-gradient(135deg, rgba(0,229,255,0.15), rgba(0,119,255,0.15));
  border: 1px solid rgba(0,229,255,0.25);
  border-top-right-radius: 4px;
  color: var(--text);
}
.msg-bubble strong { color: var(--accent); }
.msg-bubble .faculty-card {
  background: rgba(0,229,255,0.05);
  border: 1px solid rgba(0,229,255,0.2);
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 0;
  font-size: 13px;
}
.msg-bubble .faculty-card .name { font-weight: 600; color: var(--accent); font-size: 14px; }
.msg-bubble .faculty-card .detail { color: var(--muted); margin-top: 3px; }
.msg-bubble .detail span { color: var(--text); }
.typing {
  display: flex;
  gap: 5px;
  padding: 14px 18px;
  align-items: center;
}
.typing span {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--accent);
  animation: bounce 1.2s infinite;
  opacity: 0.6;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%,60%,100% { transform: translateY(0); }
  30% { transform: translateY(-6px); opacity: 1; }
}
.map-card {
  margin-top: 14px;
  border-radius: 12px;
  overflow: hidden;
  background: #080f1c;
  border: 1px solid #0077ff;
  box-shadow: 0 0 15px rgba(0,119,255,0.3);
  transition: all 0.3s ease;
}
.map-card:hover { box-shadow: 0 0 25px rgba(0,229,255,0.5); border-color: #00e5ff; }
.map-header {
  background: rgba(0,119,255,0.15);
  color: #00e5ff;
  padding: 8px 12px;
  font-family: var(--font-head);
  font-size: 13px;
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(0,119,255,0.3);
}
.input-area {
  padding: 16px 28px 20px;
  border-top: 1px solid var(--border);
  background: rgba(8,15,28,0.9);
  backdrop-filter: blur(12px);
  flex-shrink: 0;
  z-index: 20;
}
.input-row {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  background: rgba(10, 15, 30, 0.9);
  border: 1px solid #063970;
  border-radius: 14px;
  padding: 10px 14px;
  transition: all 0.3s ease;
}
.input-row:focus-within {
  border-color: #00e5ff;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.4), inset 0 0 5px rgba(0, 229, 255, 0.2);
}
.articulated-bot {
  position: absolute;
  top: -24px; left: 20px;
  width: 20px; height: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  z-index: 25;
  animation: patrolArticulated 10s linear infinite;
  filter: drop-shadow(0 0 10px rgba(0,229,255,0.8));
}
.bot-head {
  width: 14px; height: 10px;
  background: #0d1a33;
  border: 1px solid #00e5ff;
  border-radius: 4px;
  display: flex; justify-content: space-evenly; align-items: center;
  position: relative; z-index: 3;
}
.bot-torso {
  width: 12px; height: 10px;
  background: #063970;
  border-left: 1px solid #0077ff; border-right: 1px solid #0077ff;
  position: relative; z-index: 2;
}
.bot-eye {
  width: 2px; height: 3px;
  background: #fff; border-radius: 50%;
  box-shadow: 0 0 4px #00e5ff;
  animation: tinyBlink 3s infinite;
}
.bot-arm, .bot-leg { position: absolute; background: #00e5ff; border-radius: 2px; }
.bot-arm { width: 3px; height: 8px; top: 1px; transform-origin: top center; }
.bot-arm.left { left: -4px; animation: swingArmLeft 0.5s infinite alternate ease-in-out; }
.bot-arm.right { right: -4px; animation: swingArmRight 0.5s infinite alternate ease-in-out; }
.bot-leg { width: 4px; height: 9px; top: 9px; transform-origin: top center; }
.bot-leg.left { left: 1px; animation: swingLegLeft 0.5s infinite alternate ease-in-out; }
.bot-leg.right { right: 1px; animation: swingLegRight 0.5s infinite alternate ease-in-out; }
@keyframes swingArmLeft { 0% { transform: rotate(30deg); } 100% { transform: rotate(-30deg); } }
@keyframes swingArmRight { 0% { transform: rotate(-30deg); } 100% { transform: rotate(30deg); } }
@keyframes swingLegLeft { 0% { transform: rotate(-30deg); } 100% { transform: rotate(30deg); } }
@keyframes swingLegRight { 0% { transform: rotate(30deg); } 100% { transform: rotate(-30deg); } }
@keyframes patrolArticulated {
  0% { left: 15px; transform: scaleX(1); }
  45% { left: 180px; transform: scaleX(1); }
  50% { left: 180px; transform: scaleX(-1); }
  95% { left: 15px; transform: scaleX(-1); }
  100% { left: 15px; transform: scaleX(1); }
}
@keyframes tinyBlink { 0%, 96%, 98% { transform: scaleY(1); } 97% { transform: scaleY(0.1); } }
#userInput {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: var(--text);
  font-family: var(--font-body);
  font-size: 14px;
  resize: none;
  max-height: 120px;
  min-height: 24px;
  line-height: 1.5;
}
#userInput::placeholder { color: var(--muted); }
#sendBtn {
  background: var(--accent);
  border: none;
  color: var(--bg);
  width: 36px; height: 36px;
  border-radius: 9px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-weight: bold;
}
#sendBtn.pulse {
  animation: buttonPulse 1.5s infinite;
  background: #00e5ff;
  box-shadow: 0 0 10px #00e5ff;
}
@keyframes buttonPulse {
  0% { transform: scale(1); box-shadow: 0 0 5px #00e5ff; }
  50% { transform: scale(1.1); box-shadow: 0 0 20px #00e5ff; }
  100% { transform: scale(1); box-shadow: 0 0 5px #00e5ff; }
}
#sendBtn:hover { background: #33eeff; transform: scale(1.05); }
#sendBtn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
.input-hint {
  font-size: 11px;
  color: var(--muted);
  margin-top: 8px;
  text-align: center;
}
@media (max-width: 640px) {
  .sidebar { display: none; }
  .messages { padding: 16px; }
  .input-area { padding: 12px 16px 16px; }
}
</style>
</head>
<body>
<canvas id="bgCanvas"></canvas>
<header>
  <div class="logo-icon">🎓</div>
  <div class="header-text">
    <h1>CU_SMART_ASSISTANT</h1>
    <p>Chandigarh University · Faculty &amp; Campus Info</p>
  </div>
  <div class="status-dot">ONLINE</div>
</header>
<div class="main">
  <aside class="sidebar">
    <div class="sidebar-title">⚡ Quick Questions</div>
    <div class="sidebar-section">
      <div class="sidebar-title" style="font-size:9px; margin-top:4px;">🧑🏫 Faculty</div>
      <button class="quick-btn" onclick="askQuestion('Who is the faculty coordinator for MBA?')"><span class="q-icon">💼</span>MBA coordinator?</button>
      <button class="quick-btn" onclick="askQuestion('Who handles CSE AIML program?')"><span class="q-icon">🤖</span>CSE AIML faculty?</button>
      <button class="quick-btn" onclick="askQuestion('Give me contact of law department faculty')"><span class="q-icon">⚖️</span>Law dept contact?</button>
      <button class="quick-btn" onclick="askQuestion('Who is the coordinator for B.Arch?')"><span class="q-icon">🏛️</span>B.Arch coordinator?</button>
      <button class="quick-btn" onclick="askQuestion('Who handles Pharmacy program?')"><span class="q-icon">💊</span>Pharmacy faculty?</button>
      <button class="quick-btn" onclick="askQuestion('List all faculty in Block B4')"><span class="q-icon">🏢</span>Block B4 faculty?</button>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-title" style="font-size:9px; margin-top:4px;">📍 Location</div>
      <button class="quick-btn" onclick="askQuestion('Where is the fashion design department located?')"><span class="q-icon">👗</span>Fashion Design room?</button>
      <button class="quick-btn" onclick="askQuestion('Where can I find the BCA department?')"><span class="q-icon">💻</span>BCA department?</button>
      <button class="quick-btn" onclick="askQuestion('Which block is UIE located in?')"><span class="q-icon">⚙️</span>UIE block location?</button>
    </div>
    <div class="sidebar-section">
      <div class="sidebar-title" style="font-size:9px; margin-top:4px;">📧 Contact</div>
      <button class="quick-btn" onclick="askQuestion('What is the email of Civil Engineering coordinator?')"><span class="q-icon">✉️</span>Civil Engg email?</button>
      <button class="quick-btn" onclick="askQuestion('Phone number of Mechanical Engineering faculty?')"><span class="q-icon">📞</span>Mech Engg phone?</button>
    </div>
  </aside>
  <div class="chat-area">
    <div class="messages" id="messages">
      <div class="welcome">
        <span class="welcome-icon">🤖</span>
        <h2>Hey there Buddy ...</h2>
        <div style="font-weight: bold; color: var(--accent); font-size: 13px; margin-bottom: 12px; letter-spacing: 0.05em;">
          ✨ Built by Sudipta, Suraj, Daniel, and Avishek ✨
        </div>
        <p>I know all the faculty coordinators, their emails, phone numbers, room numbers and block locations. Ask me anything about your university!</p>
      </div>
    </div>
    <div class="input-area">
      <div class="input-row" style="position: relative;">
        <div class="articulated-bot">
          <div class="bot-head">
            <div class="bot-eye"></div><div class="bot-eye"></div>
          </div>
          <div class="bot-torso">
            <div class="bot-arm left"></div>
            <div class="bot-arm right"></div>
            <div class="bot-leg left"></div>
            <div class="bot-leg right"></div>
          </div>
        </div>
        <textarea id="userInput" placeholder="Ask me about any faculty, department, or coordinator..." rows="1"></textarea>
        <button id="sendBtn" onclick="sendMessage()">➤</button>
      </div>
      <div class="input-hint">Press Enter to send · Shift+Enter for new line</div>
    </div>
  </div>
</div>
<script>
const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
let conversationHistory = [];

function askQuestion(q) { inputEl.value = q; sendMessage(); }

function addMessage(role, text) {
  const welcome = messagesEl.querySelector('.welcome');
  if (welcome) welcome.remove();
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  const avatar = role === 'bot' ? '🤖' : '👤';
  div.innerHTML = `<div class="msg-avatar">${avatar}</div><div class="msg-bubble">${formatText(text)}</div>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function formatText(text) {
  text = text.replace(/Name:/gi, '<strong>Name:</strong>');
  text = text.replace(/Email:/gi, '<strong>Email:</strong>');
  text = text.replace(/Phone:/gi, '<strong>Phone:</strong>');
  text = text.replace(/Room:/gi, '<strong>Room:</strong>');
  text = text.replace(/Block:/gi, '<strong>Block:</strong>');
  text = text.replace(/Program:/gi, '<strong>Program:</strong>');
  text = text.replace(/Institute:/gi, '<strong>Institute:</strong>');
  text = text.replace(/\\[MAP:\\s*([^\\]]+)\\]/gi, function(match, location) {
    const query = encodeURIComponent(`Chandigarh University ${location}`);
    return `<div class="map-card"><div class="map-header">📍 LOCATION TARGET: ${location.toUpperCase()}</div><iframe width="100%" height="220" frameborder="0" style="border:0" src="https://maps.google.com/maps?q=${query}&t=&z=17&ie=UTF8&iwloc=&output=embed" allowfullscreen></iframe></div>`;
  });
  return text.split('\\n').join('<br>');
}

function addTyping() {
  const welcome = messagesEl.querySelector('.welcome');
  if (welcome) welcome.remove();
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.id = 'typing-indicator';
  div.innerHTML = `<div class="msg-avatar">🤖</div><div class="msg-bubble"><div class="typing"><span></span><span></span><span></span></div></div>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;
  inputEl.value = '';
  inputEl.style.height = 'auto';
  sendBtn.disabled = true;
  addMessage('user', text);
  conversationHistory.push({ role: 'user', content: text });
  const typingEl = addTyping();
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: conversationHistory })
    });
    if (!response.ok) throw new Error(`Server returned ${response.status}`);
    const data = await response.json();
    typingEl.remove();
    const reply = data.response || 'Sorry, I could not get a response. Please try again.';
    conversationHistory.push({ role: 'assistant', content: reply });
    addMessage('bot', reply);
  } catch (err) {
    console.error("Chat error:", err);
    typingEl.remove();
    addMessage('bot', 'Connection error. Make sure the backend server and Gemini API are configured correctly.');
    conversationHistory.pop();
  }
  sendBtn.disabled = false;
  inputEl.focus();
}

inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
  if (inputEl.value.trim().length > 0) { sendBtn.classList.add('pulse'); }
  else { sendBtn.classList.remove('pulse'); }
});

const canvas = document.getElementById('bgCanvas');
const ctx = canvas.getContext('2d');
let width, height, particles = [];
const mouse = { x: null, y: null, radius: 150 };
window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });
function initCanvas() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
  particles = [];
  let n = (width * height) / 12000;
  for (let i = 0; i < n; i++) {
    particles.push({ x: Math.random()*width, y: Math.random()*height, vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5, size: Math.random()*2+1 });
  }
}
function drawParticles() {
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = 'rgba(0, 229, 255, 0.5)';
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if (p.x < 0 || p.x > width) p.vx *= -1;
    if (p.y < 0 || p.y > height) p.vy *= -1;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
    if (mouse.x != null) {
      let dx = mouse.x - p.x, dy = mouse.y - p.y;
      let dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < mouse.radius) {
        ctx.beginPath();
        ctx.strokeStyle = `rgba(0, 229, 255, ${1 - dist/mouse.radius})`;
        ctx.lineWidth = 1;
        ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
      }
    }
  });
  requestAnimationFrame(drawParticles);
}
window.addEventListener('resize', initCanvas);
initCanvas(); drawParticles();
</script>
</body>
</html>"""

# ──────────────────────────────────────────────────────────────────
# FLASK APP
# ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load .env from the same directory as this script (optional)
_script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_script_dir, '.env'), override=True)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))

SYSTEM_INSTRUCTION = f"""
You are CU Smart Assistant, an AI chatbot for Chandigarh University students.
Your job is to help students find information about faculty members, their contact details, and locations.

FACULTY DATABASE:
{json.dumps(FACULTY_DATA, indent=2)}

You have access to a database of faculty information provided in your context.
If a student asks about a specific person, department, or location, search the context and provide clear, accurate answers.
Format the faculty details cleanly using these exact labels: "Name:", "Email:", "Phone:", "Room:", "Block:", "Program:", "Institute:".

*** ADDED FEATURE: MAP INTEGRATION ***
If a user asks where a specific block or building is located (for example, "Where is Block B4?" or "Show me Block C1" or "Where is the BCA department located?"), you must append a map token at the very end of your response.
The map token must look exactly like this: [MAP: Block B4]
Replace "Block B4" with the correct block name they are looking for (e.g., [MAP: Block C1], [MAP: Block D8], [MAP: UIE Building]).

Always be polite, concise, and helpful. If you don't know the answer, just say you don't have that information.
Never make up or hallucinate phone numbers or emails.
"""

response_cache = {}

def local_faculty_search(messages, is_fallback=False):
    if not messages: return None
    latest_msg = messages[-1]['content'].lower()
    stop_words = {"who","what","where","is","the","faculty","of","for","coordinator","department","can","find","i","a","an"}
    search_terms = [w for w in latest_msg.split() if w not in stop_words and len(w) > 2]
    matches = []
    for fac in FACULTY_DATA:
        fac_text = f"{fac.get('name')} {fac.get('program')} {fac.get('institute')} {fac.get('block')}".lower()
        if any(term in fac_text for term in search_terms):
            matches.append(f"Name: {fac.get('name')}\nProgram: {fac.get('program')}\nEmail: {fac.get('email')}\nPhone: {fac.get('phone')}\nRoom: {fac.get('room')}\nBlock: {fac.get('block')}")
    matches = list(dict.fromkeys(matches))
    if not matches: return None
    prefix = "⚠️ *Google AI is Rate Limited. Local Offline Backup found:*" if is_fallback else "🔌 *Offline Mode. Local search found:*"
    return prefix + "\n\n" + "\n\n".join(matches[:3])

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    # Re-read .env on every request so dropping a new .env file works instantly
    load_dotenv(os.path.join(_script_dir, '.env'), override=True)

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    data = request.json or {}
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    # Offline mode
    if not api_key or api_key in ("your_api_key_here", "") or api_key.strip().lower() == "offline":
        result = local_faculty_search(messages, is_fallback=False)
        return jsonify({"response": result or "🔌 *Offline Mode.* No exact match found. Try a faculty name, program, or block."})

    genai.configure(api_key=api_key)

    cache_key = json.dumps(messages)
    if cache_key in response_cache:
        return jsonify({"response": response_cache[cache_key]})

    try:
        gemini_messages = [
            {"role": "user" if m['role'] == 'user' else "model", "parts": [m['content']]}
            for m in messages
        ]
        history = gemini_messages[:-1] if len(gemini_messages) > 1 else []
        latest = gemini_messages[-1]['parts'][0]

        try:
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_INSTRUCTION)
            response = model.start_chat(history=history).send_message(latest)
        except Exception as e:
            if "404" in str(e) and "gemini-1.5-flash is not found" in str(e):
                model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_INSTRUCTION)
                response = model.start_chat(history=history).send_message(latest)
            else:
                raise

        response_cache[cache_key] = response.text
        return jsonify({"response": response.text})

    except Exception as e:
        err = str(e)
        if any(k in err for k in ("API key not valid", "400", "403", "API key")):
            return jsonify({"response": f"⚠️ **Invalid API Key.** Error: {err}"})
        if "429" in err or "quota" in err.lower():
            result = local_faculty_search(messages, is_fallback=True)
            if result: return jsonify({"response": result})
            return jsonify({"response": "⏳ **Rate limited!** Wait ~60 seconds then try again."})
        return jsonify({"response": f"⚠️ **API Error:** {err}"})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  CU Smart Assistant — Single File Edition")
    print("  Open: http://127.0.0.1:5000")
    print("="*60 + "\n")
    Timer(1.0, open_browser).start()
    app.run(debug=False, port=5000)
