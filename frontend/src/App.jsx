// frontend/src/App.jsx
import React, { useState } from "react";
import {
  Calendar,
  BookOpen,
  Users,
  LogOut,
  Search,
  Plus,
  Trash2,
  Eye,
  EyeOff,
  Shield,
  AlertCircle,
  CheckCircle,
  User,
  Sparkles,
} from "lucide-react";

import Chatbot from "./components/Chatbot"; // single AI Advisor chatbot

// ============================================================================
// SECURITY CONFIGURATION
// ============================================================================

const COMMON_PASSWORDS = [
  "password",
  "123456",
  "12345678",
  "qwerty",
  "abc123",
  "monkey",
];

const hashPassword = (password) => "$2b$10$" + btoa(password).substring(0, 53);
const verifyPassword = (password, hash) => hashPassword(password) === hash;

// ============================================================================
// DATABASE INITIALIZATION
// ============================================================================

const initializeDatabase = () => ({
  users: [
    {
      id: 1,
      email: "student@umgc.edu",
      username: "johndoe",
      password: hashPassword("StudentPass123!"),
      name: "John Doe",
      role: "student",
      studentNumber: "S12345",
      major: "Computer Science",
      year: 2024,
      createdAt: "2025-10-01",
      lastLogin: "2025-11-10",
      completedCourses: ["CMSC210", "CMSC215"],
      currentGPA: 3.5,
    },
    {
      id: 2,
      email: "admin@umgc.edu",
      username: "drsmith",
      password: hashPassword("AdminPass123!"),
      name: "Dr. Smith",
      role: "admin",
      employeeId: "E001",
      department: "Computer Science",
      createdAt: "2025-09-15",
      lastLogin: "2025-11-10",
    },
  ],
  departments: [
    { id: 1, name: "Computer Science", code: "CMSC" },
    { id: 2, name: "Mathematics", code: "MATH" },
  ],
  courses: [
    {
      id: 1,
      code: "CMSC495",
      title: "CS Capstone",
      credits: 3,
      department: "Computer Science",
      description: "Senior capstone",
      capacity: 30,
      enrolled: 18,
      prerequisites: ["CMSC330"],
    },
    {
      id: 2,
      code: "CMSC330",
      title: "Programming Languages",
      credits: 3,
      department: "Computer Science",
      description: "Language concepts",
      capacity: 25,
      enrolled: 20,
      prerequisites: ["CMSC220"],
    },
    {
      id: 3,
      code: "CMSC220",
      title: "Data Structures",
      credits: 3,
      department: "Computer Science",
      description: "Data structures",
      capacity: 30,
      enrolled: 22,
      prerequisites: ["CMSC210"],
    },
    {
      id: 4,
      code: "CMSC351",
      title: "Algorithms",
      credits: 3,
      department: "Computer Science",
      description: "Algorithm design",
      capacity: 28,
      enrolled: 15,
      prerequisites: ["CMSC220"],
    },
  ],
  enrollments: [
    {
      id: 1,
      studentId: 1,
      courseId: 1,
      status: "enrolled",
      enrolledDate: "2025-10-15",
    },
  ],
  failedLogins: [],
  galleryImages: [
    {
      id: 1,
      title: "Library",
      url: "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400",
      description: "UMGC Library",
    },
    {
      id: 2,
      title: "Computer Lab",
      url: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400",
      description: "Computing Facilities",
    },
  ],
});

// ============================================================================
// MAIN APPLICATION COMPONENT
// ============================================================================

export default function App() {
  const [db, setDb] = useState(initializeDatabase());
  const [currentUser, setCurrentUser] = useState(null);
  const [view, setView] = useState("login");
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDept, setSelectedDept] = useState("all");
  const [notification, setNotification] = useState(null);

  const validatePassword = (password) => {
    const errors = [];
    if (password.length < 12) errors.push("Min 12 characters");
    if (!/[A-Z]/.test(password)) errors.push("Uppercase required");
    if (!/[a-z]/.test(password)) errors.push("Lowercase required");
    if (!/[0-9]/.test(password)) errors.push("Number required");
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password))
      errors.push("Special char required");
    if (COMMON_PASSWORDS.some((c) => password.toLowerCase().includes(c)))
      errors.push("Too common");
    return errors;
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleLogin = (username, password) => {
    const user =
      db.users.find((u) => u.username === username || u.email === username) ||
      null;

    if (!user || !verifyPassword(password, user.password)) {
      setDb((prev) => ({
        ...prev,
        failedLogins: [
          ...prev.failedLogins,
          {
            timestamp: new Date().toISOString(),
            username,
            ipAddress: "192.168.1.100",
            reason: !user ? "User not found" : "Invalid password",
          },
        ],
      }));
      showNotification("Invalid credentials", "error");
      return;
    }

    setCurrentUser(user);
    setView(user.role === "admin" ? "admin" : "dashboard");
    showNotification("Welcome " + user.name + "!", "success");
  };

  const handleRegister = (userData) => {
    const { email, username, password, confirmPassword, name, role } = userData;

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showNotification("Invalid email", "error");
      return false;
    }

    if (!/^[a-zA-Z0-9_]{3,20}$/.test(username)) {
      showNotification("Invalid username", "error");
      return false;
    }

    if (db.users.some((u) => u.email === email)) {
      showNotification("Email exists", "error");
      return false;
    }

    if (db.users.some((u) => u.username === username)) {
      showNotification("Username taken", "error");
      return false;
    }

    const errors = validatePassword(password);
    if (errors.length > 0) {
      showNotification(errors[0], "error");
      return false;
    }

    if (password !== confirmPassword) {
      showNotification("Passwords mismatch", "error");
      return false;
    }

    const newUser = {
      id: db.users.length + 1,
      email,
      username,
      password: hashPassword(password),
      name,
      role: role || "student",
      createdAt: new Date().toISOString(),
      lastLogin: null,
      studentNumber:
        role === "student" ? "S" + (10000 + db.users.length) : undefined,
      major: role === "student" ? "Undeclared" : undefined,
      completedCourses: role === "student" ? [] : undefined,
      currentGPA: role === "student" ? 0.0 : undefined,
    };

    setDb((prev) => ({ ...prev, users: [...prev.users, newUser] }));
    showNotification("Registration successful!", "success");
    return true;
  };

  const getCourseRecommendations = () => {
    if (!currentUser || currentUser.role !== "student") return [];
    const completed = currentUser.completedCourses || [];
    return db.courses
      .filter(
        (c) =>
          !db.enrollments.some(
            (e) =>
              e.studentId === currentUser.id &&
              e.courseId === c.id &&
              e.status === "enrolled"
          ) &&
          c.prerequisites.every((p) => completed.includes(p)) &&
          c.department === currentUser.major
      )
      .slice(0, 3)
      .map((c) => ({
        ...c,
        reason:
          c.prerequisites.length > 0
            ? "Prerequisites met"
            : "Foundation course",
      }));
  };

  const getEnrolledCourses = () => {
    if (!currentUser) return [];
    return db.enrollments
      .filter(
        (e) => e.studentId === currentUser.id && e.status === "enrolled"
      )
      .map((e) => db.courses.find((c) => c.id === e.courseId))
      .filter(Boolean);
  };

  const isEnrolled = (courseId) =>
    db.enrollments.some(
      (e) =>
        e.studentId === currentUser.id &&
        e.courseId === courseId &&
        e.status === "enrolled"
    );

  const handleEnroll = (courseId) => {
    const course = db.courses.find((c) => c.id === courseId);
    if (!course) return;
    if (course.enrolled >= course.capacity) {
      showNotification("Course full", "error");
      return;
    }

    setDb((prev) => ({
      ...prev,
      enrollments: [
        ...prev.enrollments,
        {
          id: prev.enrollments.length + 1,
          studentId: currentUser.id,
          courseId,
          status: "enrolled",
          enrolledDate: new Date().toISOString().split("T")[0],
        },
      ],
      courses: prev.courses.map((c) =>
        c.id === courseId ? { ...c, enrolled: c.enrolled + 1 } : c
      ),
    }));
    showNotification("Enrolled successfully", "success");
  };

  const handleDrop = (courseId) => {
    setDb((prev) => ({
      ...prev,
      enrollments: prev.enrollments.map((e) =>
        e.studentId === currentUser.id && e.courseId === courseId
          ? { ...e, status: "dropped" }
          : e
      ),
      courses: prev.courses.map((c) =>
        c.id === courseId ? { ...c, enrolled: c.enrolled - 1 } : c
      ),
    }));
    showNotification("Course dropped", "success");
  };

  // ========================================================================
  // VIEW ROUTING
  // ========================================================================

  if (view === "login") {
    return (
      <LoginPage
        onLogin={handleLogin}
        onRegister={handleRegister}
        notification={notification}
        validatePassword={validatePassword}
      />
    );
  }

  if (view === "dashboard") {
    return (
      <>
        <StudentDashboard
          currentUser={currentUser}
          db={db}
          enrolledCourses={getEnrolledCourses()}
          recommendations={getCourseRecommendations()}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          selectedDept={selectedDept}
          setSelectedDept={setSelectedDept}
          isEnrolled={isEnrolled}
          onEnroll={handleEnroll}
          onDrop={handleDrop}
          onLogout={() => {
            setCurrentUser(null);
            setView("login");
            showNotification("Logged out", "success");
          }}
        />

        {/* Single AI Advisor chatbot (combined help + advisor) */}
        <Chatbot currentUser={currentUser} />

        {notification && (
          <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
            <div
              className={
                "px-6 py-4 rounded-lg shadow-xl flex items-center space-x-3 text-white " +
                (notification.type === "success"
                  ? "bg-green-500"
                  : "bg-red-500")
              }
            >
              {notification.type === "success" ? (
                <CheckCircle className="h-5 w-5" />
              ) : (
                <AlertCircle className="h-5 w-5" />
              )}
              <span>{notification.message}</span>
            </div>
          </div>
        )}
      </>
    );
  }

  if (view === "admin") {
    return (
      <AdminPanel
        currentUser={currentUser}
        db={db}
        setDb={setDb}
        showNotification={showNotification}
        onLogout={() => {
          setCurrentUser(null);
          setView("login");
          showNotification("Logged out", "success");
        }}
      />
    );
  }

  return null;
}

// ============================================================================
// LOGIN PAGE COMPONENT
// ============================================================================

function LoginPage({ onLogin, onRegister, notification, validatePassword }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);

  if (isRegistering) {
    return (
      <RegistrationForm
        onBack={() => setIsRegistering(false)}
        onRegister={onRegister}
        validatePassword={validatePassword}
        notification={notification}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <BookOpen className="mx-auto h-12 w-12 text-indigo-600 mb-2" />
          <h1 className="text-3xl font-bold text-gray-900">OCRS</h1>
          <p className="text-gray-600 mt-2">Online Course Registration</p>
          <div className="flex items-center justify-center space-x-2 mt-3">
            <Sparkles className="h-4 w-4 text-indigo-500" />
            <span className="text-xs text-indigo-600 font-semibold">
              AI-Powered
            </span>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-indigo-500"
              placeholder="johndoe"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-indigo-500"
                placeholder="••••••••"
              />
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2"
                type="button"
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>

          <button
            onClick={() => onLogin(username, password)}
            className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
          >
            Sign In
          </button>
          <button
            onClick={() => setIsRegistering(true)}
            className="w-full bg-gray-100 text-gray-700 py-2 rounded-md hover:bg-gray-200"
          >
            Create Account
          </button>
        </div>

        <div className="mt-6 text-sm text-gray-600 bg-gray-50 p-4 rounded-md">
          <p className="font-semibold mb-2">Demo:</p>
          <p>Student: johndoe / StudentPass123!</p>
          <p>Admin: drsmith / AdminPass123!</p>
        </div>
      </div>

      {notification && (
        <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
          <div
            className={
              "px-6 py-4 rounded-lg shadow-xl flex items-center space-x-3 text-white " +
              (notification.type === "success"
                ? "bg-green-500"
                : "bg-red-500")
            }
          >
            {notification.type === "success" ? (
              <CheckCircle className="h-5 w-5" />
            ) : (
              <AlertCircle className="h-5 w-5" />
            )}
            <span>{notification.message}</span>
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// REGISTRATION FORM COMPONENT
// ============================================================================

function RegistrationForm({
  onBack,
  onRegister,
  validatePassword,
  notification,
}) {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
    name: "",
    role: "student",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState([]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md max-h-screen overflow-y-auto">
        <div className="flex justify-between mb-6">
          <h2 className="text-2xl font-bold">Create Account</h2>
          <button onClick={onBack} className="text-indigo-600">
            Back
          </button>
        </div>

        <div className="space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            value={formData.name}
            onChange={(e) =>
              setFormData({ ...formData, name: e.target.value })
            }
            className="w-full px-3 py-2 border rounded-md"
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
            className="w-full px-3 py-2 border rounded-md"
          />
          <input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) =>
              setFormData({ ...formData, username: e.target.value })
            }
            className="w-full px-3 py-2 border rounded-md"
          />

          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value });
                setPasswordStrength(validatePassword(e.target.value));
              }}
              className="w-full px-3 py-2 border rounded-md"
            />
            <button
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2"
              type="button"
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5" />
              ) : (
                <Eye className="h-5 w-5" />
              )}
            </button>
          </div>

          {formData.password && passwordStrength.length > 0 && (
            <div className="text-xs text-red-600 space-y-1">
              {passwordStrength.map((e, i) => (
                <div key={i}>• {e}</div>
              ))}
            </div>
          )}

          <input
            type={showPassword ? "text" : "password"}
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={(e) =>
              setFormData({ ...formData, confirmPassword: e.target.value })
            }
            className="w-full px-3 py-2 border rounded-md"
          />

          <button
            onClick={() => {
              if (onRegister(formData)) onBack();
            }}
            className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
          >
            Create Account
          </button>
        </div>
      </div>

      {notification && (
        <div className="fixed top-20 left-1/2 transform -translate-x-1/2 z-50">
          <div
            className={
              "px-6 py-4 rounded-lg shadow-xl flex items-center space-x-3 text-white " +
              (notification.type === "success"
                ? "bg-green-500"
                : "bg-red-500")
            }
          >
            {notification.type === "success" ? (
              <CheckCircle className="h-5 w-5" />
            ) : (
              <AlertCircle className="h-5 w-5" />
            )}
            <span>{notification.message}</span>
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// STUDENT DASHBOARD COMPONENT
// ============================================================================

function StudentDashboard({
  currentUser,
  db,
  enrolledCourses,
  recommendations,
  searchTerm,
  setSearchTerm,
  selectedDept,
  setSelectedDept,
  isEnrolled,
  onEnroll,
  onDrop,
  onLogout,
}) {
  const [activeTab, setActiveTab] = useState("courses");
  const availableCourses = db.courses.filter(
    (c) =>
      (c.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.title.toLowerCase().includes(searchTerm.toLowerCase())) &&
      (selectedDept === "all" || c.department === selectedDept)
  );

  return (
    <div className="min-h-screen bg-gray-50 flex justify-center">
      <div className="w-full max-w-7xl">
        <nav className="bg-indigo-600 text-white p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-6 w-6" />
              <span className="text-xl font-bold">OCRS</span>
            </div>
            <div className="flex items-center space-x-6">
              <button
                onClick={() => setActiveTab("courses")}
                className={
                  "px-3 py-1 rounded " +
                  (activeTab === "courses" ? "bg-indigo-700" : "")
                }
              >
                Courses
              </button>
              <button
                onClick={() => setActiveTab("recommendations")}
                className={
                  "px-3 py-1 rounded flex items-center space-x-1 " +
                  (activeTab === "recommendations" ? "bg-indigo-700" : "")
                }
              >
                <Sparkles className="h-4 w-4" />
                <span>AI Recommendations</span>
              </button>
              <span>Welcome, {currentUser.name}</span>
              <button
                onClick={onLogout}
                className="flex items-center space-x-1 hover:bg-indigo-700 px-3 py-1 rounded"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto p-6">
          {activeTab === "recommendations" ? (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <Sparkles className="h-8 w-8" />
                  <h2 className="text-2xl font-bold">
                    AI-Powered Recommendations
                  </h2>
                </div>
                <p>Based on your academic history</p>
              </div>

              {recommendations.length > 0 ? (
                <div className="bg-white rounded-lg shadow p-6 space-y-4">
                  {recommendations.map((course) => (
                    <div
                      key={course.id}
                      className="border-2 border-indigo-200 rounded-lg p-4 bg-indigo-50"
                    >
                      <div className="flex justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <h3 className="font-bold text-lg">
                              {course.code}
                            </h3>
                            <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded">
                              RECOMMENDED
                            </span>
                          </div>
                          <p className="text-gray-700">{course.title}</p>
                          <p className="text-sm text-gray-600">
                            {course.description}
                          </p>
                          <div className="flex items-center space-x-4 mt-2 text-sm">
                            <span>{course.credits} credits</span>
                            <span>
                              {course.enrolled}/{course.capacity} enrolled
                            </span>
                          </div>
                          <p className="text-sm text-green-700 mt-2">
                            ✓ {course.reason}
                          </p>
                        </div>
                        <button
                          onClick={() => onEnroll(course.id)}
                          disabled={isEnrolled(course.id)}
                          className={
                            "px-4 py-2 rounded flex items-center space-x-1 " +
                            (isEnrolled(course.id)
                              ? "bg-gray-300"
                              : "bg-indigo-600 text-white hover:bg-indigo-700")
                          }
                        >
                          <Plus className="h-4 w-4" />
                          <span>
                            {isEnrolled(course.id) ? "Enrolled" : "Enroll"}
                          </span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-white rounded-lg shadow p-8 text-center">
                  <Sparkles className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">No Recommendations</h3>
                  <p className="text-gray-600">
                    Complete more courses to get recommendations
                  </p>
                </div>
              )}
            </div>
          ) : (
            <>
              <div className="grid grid-cols-3 gap-6 mb-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Enrolled Courses</p>
                      <p className="text-3xl font-bold text-indigo-600">
                        {enrolledCourses.length}
                      </p>
                    </div>
                    <BookOpen className="h-12 w-12 text-indigo-200" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Total Credits</p>
                      <p className="text-3xl font-bold text-green-600">
                        {enrolledCourses.reduce((s, c) => s + c.credits, 0)}
                      </p>
                    </div>
                    <Calendar className="h-12 w-12 text-green-200" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Current GPA</p>
                      <p className="text-3xl font-bold text-purple-600">
                        {(currentUser.currentGPA || 0).toFixed(2)}
                      </p>
                    </div>
                    <Users className="h-12 w-12 text-purple-200" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <h2 className="text-xl font-bold mb-4">My Courses</h2>
                {enrolledCourses.length > 0 ? (
                  <div className="space-y-3">
                    {enrolledCourses.map((course) => (
                      <div
                        key={course.id}
                        className="flex justify-between items-center p-4 bg-gray-50 rounded-lg"
                      >
                        <div>
                          <h3 className="font-bold">
                            {course.code} - {course.title}
                          </h3>
                          <p className="text-sm text-gray-600">
                            {course.credits} credits • {course.department}
                          </p>
                        </div>
                        <button
                          onClick={() => onDrop(course.id)}
                          className="flex items-center space-x-1 px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                        >
                          <Trash2 className="h-4 w-4" />
                          <span>Drop</span>
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-4">
                    No enrolled courses yet
                  </p>
                )}
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-bold">Available Courses</h2>
                  <div className="flex space-x-3">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                      <input
                        type="text"
                        placeholder="Search courses..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-9 pr-3 py-2 border rounded-md focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                    <select
                      value={selectedDept}
                      onChange={(e) => setSelectedDept(e.target.value)}
                      className="px-3 py-2 border rounded-md focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="all">All Departments</option>
                      {db.departments.map((dept) => (
                        <option key={dept.id} value={dept.name}>
                          {dept.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="space-y-3">
                  {availableCourses.map((course) => (
                    <div
                      key={course.id}
                      className="border rounded-lg p-4 hover:bg-gray-50"
                    >
                      <div className="flex justify-between">
                        <div className="flex-1">
                          <h3 className="font-bold text-lg">
                            {course.code} - {course.title}
                          </h3>
                          <p className="text-gray-600">
                            {course.description}
                          </p>
                          <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                            <span>{course.credits} credits</span>
                            <span>{course.department}</span>
                            <span
                              className={
                                course.enrolled >= course.capacity
                                  ? "text-red-500"
                                  : "text-green-500"
                              }
                            >
                              {course.enrolled}/{course.capacity} enrolled
                            </span>
                          </div>
                          {course.prerequisites.length > 0 && (
                            <p className="text-sm text-gray-500 mt-1">
                              Prerequisites:{" "}
                              {course.prerequisites.join(", ")}
                            </p>
                          )}
                        </div>
                        <button
                          onClick={() => onEnroll(course.id)}
                          disabled={
                            isEnrolled(course.id) ||
                            course.enrolled >= course.capacity
                          }
                          className={
                            "px-4 py-2 rounded flex items-center space-x-1 " +
                            (isEnrolled(course.id)
                              ? "bg-gray-300 cursor-not-allowed"
                              : course.enrolled >= course.capacity
                              ? "bg-red-300 cursor-not-allowed"
                              : "bg-indigo-600 text-white hover:bg-indigo-700")
                          }
                        >
                          <Plus className="h-4 w-4" />
                          <span>
                            {isEnrolled(course.id)
                              ? "Enrolled"
                              : course.enrolled >= course.capacity
                              ? "Full"
                              : "Enroll"}
                          </span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// ADMIN PANEL COMPONENT
// ============================================================================

function AdminPanel({ currentUser, db, setDb, showNotification, onLogout }) {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [courseForm, setCourseForm] = useState({
    code: "",
    title: "",
    credits: 3,
    department: "",
    description: "",
    capacity: 30,
    prerequisites: "",
  });

  const handleAddCourse = () => {
    if (!courseForm.code || !courseForm.title || !courseForm.department) {
      showNotification("Fill all required fields", "error");
      return;
    }

    const newCourse = {
      id: db.courses.length + 1,
      code: courseForm.code,
      title: courseForm.title,
      credits: parseInt(courseForm.credits),
      department: courseForm.department,
      description: courseForm.description,
      capacity: parseInt(courseForm.capacity),
      enrolled: 0,
      prerequisites: courseForm.prerequisites
        ? courseForm.prerequisites.split(",").map((p) => p.trim())
        : [],
    };

    setDb((prev) => ({ ...prev, courses: [...prev.courses, newCourse] }));
    showNotification("Course added successfully", "success");
    setCourseForm({
      code: "",
      title: "",
      credits: 3,
      department: "",
      description: "",
      capacity: 30,
      prerequisites: "",
    });
  };

  const handleDeleteCourse = (courseId) => {
    setDb((prev) => ({
      ...prev,
      courses: prev.courses.filter((c) => c.id !== courseId),
    }));
    showNotification("Course deleted", "success");
  };

  return (
    <div className="min-h-screen bg-gray-50 flex justify-center">
      <div className="w-full max-w-7xl">
        <nav className="bg-indigo-600 text-white p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Shield className="h-6 w-6" />
              <span className="text-xl font-bold">OCRS Admin Panel</span>
            </div>
            <div className="flex items-center space-x-6">
              <button
                onClick={() => setActiveTab("dashboard")}
                className={
                  "px-3 py-1 rounded " +
                  (activeTab === "dashboard" ? "bg-indigo-700" : "")
                }
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab("users")}
                className={
                  "px-3 py-1 rounded " +
                  (activeTab === "users" ? "bg-indigo-700" : "")
                }
              >
                Users
              </button>
              <button
                onClick={() => setActiveTab("courses")}
                className={
                  "px-3 py-1 rounded " +
                  (activeTab === "courses" ? "bg-indigo-700" : "")
                }
              >
                Courses
              </button>
              <button
                onClick={() => setActiveTab("security")}
                className={
                  "px-3 py-1 rounded " +
                  (activeTab === "security" ? "bg-indigo-700" : "")
                }
              >
                Security
              </button>
              <span>Admin: {currentUser.name}</span>
              <button
                onClick={onLogout}
                className="flex items-center space-x-1 hover:bg-indigo-700 px-3 py-1 rounded"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto p-6">
          {activeTab === "dashboard" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">System Overview</h2>
              <div className="grid grid-cols-4 gap-6">
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Total Users</p>
                      <p className="text-3xl font-bold text-indigo-600">
                        {db.users.length}
                      </p>
                    </div>
                    <User className="h-12 w-12 text-indigo-200" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Total Courses</p>
                      <p className="text-3xl font-bold text-green-600">
                        {db.courses.length}
                      </p>
                    </div>
                    <BookOpen className="h-12 w-12 text-green-200" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Total Enrollments</p>
                      <p className="text-3xl font-bold text-purple-600">
                        {
                          db.enrollments.filter(
                            (e) => e.status === "enrolled"
                          ).length
                        }
                      </p>
                    </div>
                    <Calendar className="h-12 w-12 text-purple-200" />
                  </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow">
                  <div className="flex justify-between">
                    <div>
                      <p className="text-gray-600 text-sm">Failed Logins</p>
                      <p className="text-3xl font-bold text-red-600">
                        {db.failedLogins.length}
                      </p>
                    </div>
                    <AlertCircle className="h-12 w-12 text-red-200" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "users" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">User Management</h2>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        ID
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Name
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Email
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Username
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Role
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Created
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {db.users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {user.id}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          {user.name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {user.email}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {user.username}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <span
                            className={
                              "px-2 py-1 rounded text-xs " +
                              (user.role === "admin"
                                ? "bg-red-100 text-red-800"
                                : "bg-blue-100 text-blue-800")
                            }
                          >
                            {user.role}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {new Date(user.createdAt).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === "courses" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Course Management</h2>
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-bold mb-4">Add New Course</h3>
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Course Code"
                    value={courseForm.code}
                    onChange={(e) =>
                      setCourseForm({ ...courseForm, code: e.target.value })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="text"
                    placeholder="Course Title"
                    value={courseForm.title}
                    onChange={(e) =>
                      setCourseForm({ ...courseForm, title: e.target.value })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="number"
                    placeholder="Credits"
                    value={courseForm.credits}
                    onChange={(e) =>
                      setCourseForm({
                        ...courseForm,
                        credits: e.target.value,
                      })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="text"
                    placeholder="Department"
                    value={courseForm.department}
                    onChange={(e) =>
                      setCourseForm({
                        ...courseForm,
                        department: e.target.value,
                      })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="number"
                    placeholder="Capacity"
                    value={courseForm.capacity}
                    onChange={(e) =>
                      setCourseForm({
                        ...courseForm,
                        capacity: e.target.value,
                      })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="text"
                    placeholder="Prerequisites (comma separated)"
                    value={courseForm.prerequisites}
                    onChange={(e) =>
                      setCourseForm({
                        ...courseForm,
                        prerequisites: e.target.value,
                      })
                    }
                    className="px-3 py-2 border rounded-md"
                  />
                  <input
                    type="text"
                    placeholder="Description"
                    value={courseForm.description}
                    onChange={(e) =>
                      setCourseForm({
                        ...courseForm,
                        description: e.target.value,
                      })
                    }
                    className="px-3 py-2 border rounded-md col-span-2"
                  />
                </div>
                <button
                  onClick={handleAddCourse}
                  className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Add Course
                </button>
              </div>

              <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Code
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Title
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Credits
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Enrolled
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {db.courses.map((course) => (
                      <tr key={course.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          {course.code}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {course.title}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {course.credits}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {course.enrolled}/{course.capacity}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <button
                            onClick={() => handleDeleteCourse(course.id)}
                            className="text-red-600 hover:text-red-800"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === "security" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold">Security Audit Log</h2>
              <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Timestamp
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Username
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        IP Address
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Reason
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {db.failedLogins.map((log, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {new Date(log.timestamp).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {log.username}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {log.ipAddress}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          {log.reason}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {db.failedLogins.length === 0 && (
                  <p className="text-center text-gray-500 py-8">
                    No failed login attempts
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
