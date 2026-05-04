import { Anchor } from 'lucide-react';

export default function ChatHeader() {
  return (
    <div className="bg-green-600 text-white p-4 shadow-lg">
      <div className="max-w-4xl mx-auto flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center">
          <Anchor className="w-6 h-6 text-green-600" />
        </div>
        <div>
          <h1 className="font-semibold text-lg">BP2TL Jakarta Helpdesk</h1>
          <p className="text-sm text-green-100">Asisten Virtual Perizinan</p>
        </div>
      </div>
    </div>
  );
}
