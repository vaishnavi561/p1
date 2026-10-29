import React from 'react';

export default function VitalsGrid({ selectedMember }) {
  const stats = [
    { label: 'A1C', value: selectedMember.a1c ? `${selectedMember.a1c}%` : 'Not recorded' },
    { label: 'Blood pressure', value: selectedMember.bp_systolic && selectedMember.bp_diastolic ? `${selectedMember.bp_systolic}/${selectedMember.bp_diastolic}` : 'Not recorded' },
    { label: 'Weight', value: selectedMember.weight ? `${selectedMember.weight} kg` : 'Not recorded' },
    { label: 'Height', value: selectedMember.height ? `${selectedMember.height} cm` : 'Not recorded' },
    { label: 'Age', value: selectedMember.age ?? 'Not recorded' },
  ];

  return (
    <div className="grid grid-cols-5 gap-4">
      {stats.map((stat, idx) => (
        <div key={idx} className="p-4 rounded-xl border shadow-md bg-white dark:bg-gray-900 border-rose-200 dark:border-gray-800">
          <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1">{stat.label}</div>
          <div className={`text-sm font-bold ${stat.value === 'Not recorded' ? 'text-gray-400' : 'text-gray-800 dark:text-white'}`}>{stat.value}</div>
        </div>
      ))}
    </div>
  );
}