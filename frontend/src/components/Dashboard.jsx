import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { parseApiError } from '../utils/errorHandler';
import Toast from './ui/Toast';

import AiConfigBar from './dashboard/AiConfigBar';
import MemberSidebar from './dashboard/MemberSidebar';
import AddMemberForm from './dashboard/AddMemberForm';
import MemberDetail from './dashboard/MemberDetail';

export default function Dashboard() {
  const navigate = useNavigate();
  const { isDarkMode, toggleTheme } = useTheme();
  
  const [hasAgreed, setHasAgreed] = useState(false);
  const [username, setUsername] = useState('');
  const [currentView, setCurrentView] = useState('add-member');
  const [selectedModel, setSelectedModel] = useState('Ollama');
  const [apiKey, setApiKey] = useState('');
  const [isAiConnected, setIsAiConnected] = useState(false);
  const [familyMembers, setFamilyMembers] = useState([]);
  const [selectedMember, setSelectedMember] = useState(null);
  const [chatInput, setChatInput] = useState('');
  
  const [chatHistories, setChatHistories] = useState({});
  const [isAnswering, setIsAnswering] = useState(false);

  // Edit Mode States (P2-04)
  const [isEditing, setIsEditing] = useState(false);
  const [editingMemberId, setEditingMemberId] = useState(null);

  // Form Fields
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [dob, setDob] = useState('');
  const [gender, setGender] = useState('');
  const [race, setRace] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [a1c, setA1c] = useState('');
  const [bloodPressure, setBloodPressure] = useState('');
  const [conditions, setConditions] = useState(''); 
  
  const [isScanning, setIsScanning] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [error, setError] = useState('');

  // P3-05 Toast States
  const [toastMessage, setToastMessage] = useState(null);
  const [toastType, setToastType] = useState('error');

  const modelLabel = selectedModel === 'Ollama' ? 'Qwen 1.8B' : selectedModel;

  useEffect(() => {
    const storedUser = localStorage.getItem('username');
    setUsername(storedUser || 'Guest User');
    fetchProfiles();
  }, []);

  const fetchChatHistory = async (memberId) => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await axios.get(`http://127.0.0.1:8000/api/ai-chat/?member_id=${memberId}`, { headers });
      
      if (res.data && res.data.history) {
        setChatHistories(prev => ({
          ...prev,
          [memberId]: res.data.history
        }));
      } else {
        setChatHistories(prev => ({
          ...prev,
          [memberId]: []
        }));
      }
    } catch (err) {
      console.warn("Could not fetch chat history.", err);
      setChatHistories(prev => ({
        ...prev,
        [memberId]: []
      }));
    }
  };

  const fetchProfiles = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const storedUser = localStorage.getItem('username') || '';
      const res = await axios.get(`http://127.0.0.1:8000/api/family-profiles/?username=${encodeURIComponent(storedUser)}`, { headers });
      
      const profiles = res.data || [];
      setFamilyMembers(profiles);
      
      if (profiles.length === 0) {
        setCurrentView('add-member');
      } else {
        setSelectedMember(profiles[0]);
        setCurrentView('profile-detail');
        fetchChatHistory(profiles[0].id);
      }
    } catch (err) {
      console.warn("Could not fetch database profiles. Starting fresh.");
      setFamilyMembers([]);
      setCurrentView('add-member');
    }
  };

  const handleAgree = () => {
    setHasAgreed(true);
    setCurrentView(familyMembers.length > 0 ? 'profile-detail' : 'add-member');
  };

  const handleCancelLogout = () => {
    localStorage.clear();
    navigate('/'); 
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
    setApiKey(''); 
    setIsAiConnected(false);
  };

  const handleApiKeyChange = (e) => {
    setApiKey(e.target.value);
    setIsAiConnected(false);
  };

  const handleConnectAI = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      const res = await axios.post('http://127.0.0.1:8000/api/models/health/', {
        model: selectedModel,
        api_key: apiKey
      }, { headers });

      if (res.status === 200) {
        setIsAiConnected(true);
        setToastMessage(`Successfully connected to ${selectedModel}!`);
        setToastType('success');
      }
    } catch (err) {
      console.error("AI connection health check failed:", err);
      const errorStr = parseApiError(err, `Failed to connect to ${selectedModel}. Please check your configuration.`);
      setToastMessage(errorStr);
      setToastType('error');
      setIsAiConnected(false);
    }
  };

  const handlePrescriptionScan = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setIsScanning(true);
    setError('');
    
    const formData = new FormData();
    formData.append('image', file);
    formData.append('model', selectedModel);   
    formData.append('api_key', apiKey);        

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/scan-prescription/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setConditions(res.data.extracted_text || '');
      setToastMessage("Prescription scanned successfully!");
      setToastType('success');
    } catch (err) {
      console.error("OCR scan error:", err);
      const errorStr = parseApiError(err, "OCR scan failed.");
      setError(errorStr);
      setToastMessage(errorStr);
      setToastType('error');
    } finally {
      setIsScanning(false);
      e.target.value = ''; 
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (!firstName.trim()) {
      const msg = "First name is required.";
      setError(msg);
      setToastMessage(msg);
      setToastType('error');
      return;
    }

    const storedUser = localStorage.getItem('username') || '';

    let systolic = null;
    let diastolic = null;
    if (bloodPressure.includes('/')) {
      const parts = bloodPressure.split('/');
      systolic = parseInt(parts[0].trim(), 10) || null;
      diastolic = parseInt(parts[1].trim(), 10) || null;
    }

    const memberData = {
      username: storedUser,
      name: `${firstName.trim()} ${lastName ? lastName.trim() : ''}`.trim(),
      relation: 'Family Member',
      date_of_birth: dob || null,
      height: height ? parseFloat(height) : null,
      weight: weight ? parseFloat(weight) : null,
      a1c: a1c ? parseFloat(a1c) : null,
      bp_systolic: systolic,
      bp_diastolic: diastolic,
      conditions: conditions.trim() || 'None listed'
    };

    try {
      if (isEditing) {
        const res = await axios.patch(`http://127.0.0.1:8000/api/family-profiles/${editingMemberId}/`, memberData, {
          withCredentials: true
        });
        const updatedMember = res.data;
        
        setFamilyMembers(familyMembers.map(m => m.id === editingMemberId ? updatedMember : m));
        setSelectedMember(updatedMember);
        setCurrentView('profile-detail');
        setSuccessMessage("Profile updated successfully!");
        setToastMessage("Profile updated successfully!");
        setToastType('success');
      } else {
        if (familyMembers.length >= 4) {
          const msg = "Maximum limit of 4 family members reached.";
          setError(msg);
          setToastMessage(msg);
          setToastType('error');
          return;
        }
        const res = await axios.post('http://127.0.0.1:8000/api/family-profiles/', memberData, {
          withCredentials: true
        });
        const newMember = res.data; 
        const updatedList = [...familyMembers, newMember];
        
        setFamilyMembers(updatedList);
        setSelectedMember(newMember);
        setChatHistories(prev => ({ ...prev, [newMember.id]: [] }));
        setCurrentView('profile-detail');
        setSuccessMessage("Profile saved successfully!");
        setToastMessage("Profile saved successfully!");
        setToastType('success');
      }

      setIsEditing(false);
      setEditingMemberId(null);
      setFirstName(''); setLastName(''); setDob(''); setGender('');
      setRace(''); setHeight(''); setWeight(''); setA1c(''); setBloodPressure(''); setConditions('');
    } catch (err) {
      console.error("Database save error:", err.response?.data || err);
      const errorStr = parseApiError(err, "Failed to save to database. Please check backend.");
      setError(errorStr);
      setToastMessage(errorStr);
      setToastType('error');
    }
  };

  const handleRemoveMember = async (id) => {
    const confirmed = window.confirm("Are you sure you want to delete this family member profile?");
    if (!confirmed) return;

    try {
      await axios.delete(`http://127.0.0.1:8000/api/family-profiles/${id}/`, {
        withCredentials: true
      });
      const filtered = familyMembers.filter(m => m.id !== id);
      setFamilyMembers(filtered);
      
      setChatHistories(prev => {
        const copy = { ...prev };
        delete copy[id];
        return copy;
      });

      setToastMessage("Profile deleted successfully.");
      setToastType('success');

      if (filtered.length > 0) {
        setSelectedMember(filtered[0]);
        setCurrentView('profile-detail');
      } else {
        setSelectedMember(null);
        setCurrentView('add-member');
      }
    } catch (err) {
      console.error("Failed to delete member:", err);
      const errorStr = parseApiError(err, "Failed to delete member from database.");
      setError(errorStr);
      setToastMessage(errorStr);
      setToastType('error');
    }
  };

  const handleOpenEdit = (member) => {
    setIsEditing(true);
    setEditingMemberId(member.id);
    
    const nameParts = (member.name || '').split(' ');
    setFirstName(nameParts[0] || '');
    setLastName(nameParts.slice(1).join(' ') || '');
    
    setDob(member.date_of_birth || '');
    setHeight(member.height || '');
    setWeight(member.weight || '');
    setA1c(member.a1c || '');
    setBloodPressure(
      member.bp_systolic && member.bp_diastolic 
        ? `${member.bp_systolic}/${member.bp_diastolic}` 
        : ''
    );
    setConditions(member.conditions || '');
    
    setCurrentView('add-member');
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || !selectedMember) return;

    const currentMemberId = selectedMember.id;
    const currentMessages = chatHistories[currentMemberId] || [];
    const userQuestion = chatInput.trim();
    setChatInput('');

    const newMessages = [...currentMessages, { sender: 'user', text: userQuestion }];
    
    setChatHistories(prev => ({
      ...prev,
      [currentMemberId]: newMessages
    }));
    
    setIsAnswering(true);

    try {
      const res = await axios.post('http://127.0.0.1:8000/api/ai-chat/', {
        member_id: currentMemberId,
        question: userQuestion,
        model: selectedModel,   
        api_key: apiKey        
      });
      
      const aiText = res.data.response;
      const remaining = res.data.remaining_quota;
      
      const updatedWithAI = [...newMessages, { sender: 'ai', text: aiText }];
      setChatHistories(prev => ({
        ...prev,
        [currentMemberId]: updatedWithAI
      }));

      if (remaining !== undefined) {
        console.log(`Remaining quota for member: ${remaining}`);
      }

    } catch (err) {
      console.warn("Backend chat failed.", err);
      
      let errorText = "[Error]: Could not reach backend AI endpoint.";
      if (err.response && err.response.status === 429) {
        errorText = "[Limit Reached]: You have reached the maximum question limit (100) for this profile.";
      } else {
        errorText = parseApiError(err, errorText);
      }

      setToastMessage(errorText);
      setToastType('error');

      const updatedWithError = [...newMessages, { sender: 'ai', text: errorText }];
      setChatHistories(prev => ({
        ...prev,
        [currentMemberId]: updatedWithError
      }));
    } finally {
      setIsAnswering(false);
    }
  };

  const getInitials = (fname) => {
    return fname ? fname[0].toUpperCase() : 'QF';
  };

  const getMemberQuestionCount = (memberId) => {
    const msgs = chatHistories[memberId] || [];
    return msgs.filter(m => m.sender === 'user').length;
  };

  const activeMessages = selectedMember ? (chatHistories[selectedMember.id] || []) : [];
  const activeQuestionCount = selectedMember ? getMemberQuestionCount(selectedMember.id) : 0;

  if (!hasAgreed) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-rose-50/50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors duration-200">
        <div className="max-w-2xl w-full p-10 rounded-3xl shadow-xl text-center border bg-white dark:bg-gray-900 border-rose-200 dark:border-gray-800 text-gray-900 dark:text-gray-100 transition-colors duration-200">
          <div className="w-16 h-16 bg-rose-500/10 text-rose-500 rounded-2xl flex items-center justify-center mx-auto mb-6 text-3xl">
            💚
          </div>
          <h2 className="text-3xl font-extrabold mb-2">Welcome to MedLife.ai</h2>
          <p className="text-xs mb-8 text-gray-500 dark:text-gray-400">Your intelligent medical companion dashboard</p>

          <div className="p-6 rounded-2xl text-left mb-8 border shadow-sm bg-amber-50/70 dark:bg-amber-950/20 border-amber-200/60 dark:border-amber-800/40 text-amber-950 dark:text-amber-200/90">
            <div className="text-xs font-bold uppercase tracking-wider mb-2 flex items-center">
              <span>⚠️</span> <span className="ml-2">Medical Disclaimer</span>
            </div>
            <p className="text-xs leading-relaxed">
              All information in this application is provided solely to demonstrate how AI can be used in healthcare. This information is sourced from AI engines. None of the information has been validated or approved by a healthcare professional. Please use this information only after consulting and upon the advice of a healthcare professional.
            </p>
          </div>

          <div className="flex items-center justify-center space-x-4">
            <button 
              onClick={handleAgree}
              className="px-8 py-3.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl shadow-md transition flex items-center space-x-2"
            >
              <span>Agree & Continue</span> <span>→</span>
            </button>
            <button 
              onClick={handleCancelLogout}
              className="px-6 py-3.5 font-semibold text-xs transition text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
            >
              Cancel / Logout
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden flex bg-rose-50/30 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      
      <MemberSidebar 
        familyMembers={familyMembers}
        selectedMember={selectedMember}
        onSelectMember={(member, view) => {
          if (member) setSelectedMember(member);
          setCurrentView(view);
          if (member && !chatHistories[member.id]) {
            fetchChatHistory(member.id);
          }
        }}
        currentView={currentView}
        onOpenAddMember={() => {
          setIsEditing(false);
          setEditingMemberId(null);
          setFirstName(''); setLastName(''); setDob(''); setGender('');
          setRace(''); setHeight(''); setWeight(''); setA1c(''); setBloodPressure(''); setConditions('');
          setCurrentView('add-member');
        }}
        onLogout={handleCancelLogout}
        onNavigate2FA={() => navigate('/2fa-setup')}
        username={username}
        getInitials={getInitials}
        getMemberQuestionCount={getMemberQuestionCount}
      />

      <div className="flex-1 flex flex-col h-screen overflow-y-auto">
        <AiConfigBar 
          selectedModel={selectedModel}
          onModelChange={handleModelChange}
          apiKey={apiKey}
          onApiKeyChange={handleApiKeyChange}
          isAiConnected={isAiConnected}
          onConnectAI={handleConnectAI}
          isDarkMode={isDarkMode}
          toggleTheme={toggleTheme}
        />

        <div className="flex-1 p-8 transition-colors duration-200 bg-rose-50/30 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
          {currentView === 'add-member' && (
            <AddMemberForm 
              isEditing={isEditing}
              error={error}
              successMessage={successMessage}
              onSubmit={handleAddMember}
              firstName={firstName} setFirstName={setFirstName}
              lastName={lastName} setLastName={setLastName}
              dob={dob} setDob={setDob}
              gender={gender} setGender={setGender}
              race={race} setRace={setRace}
              height={height} setHeight={setHeight}
              weight={weight} setWeight={setWeight}
              a1c={a1c} setA1c={setA1c}
              bloodPressure={bloodPressure} setBloodPressure={setBloodPressure}
              conditions={conditions} setConditions={setConditions}
              isScanning={isScanning}
              onPrescriptionScan={handlePrescriptionScan}
            />
          )}

          {currentView === 'profile-detail' && selectedMember && (
            <MemberDetail 
              selectedMember={selectedMember}
              getInitials={getInitials}
              onOpenEdit={handleOpenEdit}
              onRemoveMember={handleRemoveMember}
              modelLabel={modelLabel}
              activeMessages={activeMessages}
              isAnswering={isAnswering}
              chatInput={chatInput}
              onChatInputChange={(e) => setChatInput(e.target.value)}
              onSendMessage={handleSendMessage}
              activeQuestionCount={activeQuestionCount}
            />
          )}
        </div>
      </div>

      {/* P3-05 Toast Component Integration */}
      <Toast message={toastMessage} type={toastType} onClose={() => setToastMessage(null)} />
    </div>
  );
}