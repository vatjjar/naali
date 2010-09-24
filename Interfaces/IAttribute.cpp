/**
 *  For conditions of distribution and use, see copyright notice in license.txt
 *
 *  @file   IAttribute.cpp
 *  @brief  Abstract base class and template class for entity-component attributes.
 */

#include "StableHeaders.h"

#include "IAttribute.h"
#include "IComponent.h"
#include "AssetInterface.h"
#include "Core.h"
#include "CoreStdIncludes.h"
#include "Transform.h"

#include <QVariant>
#include <QStringList>

#include "clb/Network/DataDeserializer.h"
#include "clb/Network/DataSerializer.h"

// Implementation code for some common attributes

IAttribute::IAttribute(IComponent* owner, const char* name) :
    owner_(owner),
    name_(name),
    change_(AttributeChange::None),
    null_(false),
    metadata_(0)
{
    if (owner)
        owner->AddAttribute(this);
}

void IAttribute::Changed(AttributeChange::Type change)
{
    if (owner_)
        owner_->AttributeChanged(this, change);
}

// TOSTRING TEMPLATE IMPLEMENTATIONS.

template<> std::string Attribute<QString>::ToString() const
{
    ///\todo decode/encode XML-risky characters
    return Get().toStdString();
}

template<> std::string Attribute<bool>::ToString() const
{
    if (Get())
        return "true";
    else
        return "false";
}

template<> std::string Attribute<int>::ToString() const
{
    return ::ToString<int>(Get());
}

template<> std::string Attribute<uint>::ToString() const
{
    return ::ToString<uint>(Get());
}

template<> std::string Attribute<float>::ToString() const
{
    return ::ToString<float>(Get());
}

template<> std::string Attribute<Vector3df>::ToString() const
{
    Vector3df value = Get();
    
    return ::ToString<float>(value.x) + " " +
        ::ToString<float>(value.y) + " " +
        ::ToString<float>(value.z);
}
    
template<> std::string Attribute<Quaternion>::ToString() const
{
    Quaternion value = Get();
    
    return ::ToString<float>(value.w) + " " +
        ::ToString<float>(value.x) + " " +
        ::ToString<float>(value.y) + " " +
        ::ToString<float>(value.z);
}

template<> std::string Attribute<Color>::ToString() const
{
    Color value = Get();
    
    return ::ToString<float>(value.r) + " " +
        ::ToString<float>(value.g) + " " +
        ::ToString<float>(value.b) + " " +
        ::ToString<float>(value.a);
}

template<> std::string Attribute<Foundation::AssetReference>::ToString() const
{
    Foundation::AssetReference value = Get();
    return value.type_ + "," + value.id_;
}

template<> std::string Attribute<QVariant>::ToString() const
{
    QVariant value = Get();
    
    return value.toString().toStdString();
}

template<> std::string Attribute<QVariantList>::ToString() const
{
    QVariantList values = Get();

    std::string stringValue = "";
    for(uint i = 0; i < values.size(); i++)
    {
        stringValue += values[i].toString().toStdString();
        if(i < values.size() - 1)
            stringValue += ";";
    }
    return stringValue;
}

template<> std::string Attribute<Transform>::ToString() const
{
    QString value("");
    Transform transform = Get();
    Vector3D<float> editValues[3];
    editValues[0] = transform.position;
    editValues[1] = transform.rotation;
    editValues[2] = transform.scale;

    for(uint i = 0; i < 3; i++)
    {
        value += QString::number(editValues[i].x);
        value += ",";
        value += QString::number(editValues[i].y);
        value += ",";
        value += QString::number(editValues[i].z);
        if(i < 2)
            value += ",";
    }
    return value.toStdString();
}

// TYPENAMETOSTRING TEMPLATE IMPLEMENTATIONS.

template<> std::string Attribute<int>::TypenameToString() const
{
    return "int";
}

template<> std::string Attribute<uint>::TypenameToString() const
{
    return "uint";
}

template<> std::string Attribute<float>::TypenameToString() const
{
    return "real";
}

template<> std::string Attribute<QString>::TypenameToString() const
{
    return "string";
}

template<> std::string Attribute<bool>::TypenameToString() const
{
    return "bool";
}

template<> std::string Attribute<Vector3df>::TypenameToString() const
{
    return "vector3df";
}

template<> std::string Attribute<Quaternion>::TypenameToString() const
{
    return "quaternion";
}

template<> std::string Attribute<Color>::TypenameToString() const
{
    return "color";
}

template<> std::string Attribute<Foundation::AssetReference>::TypenameToString() const
{
    return "assetreference";
}

template<> std::string Attribute<QVariant>::TypenameToString() const
{
    return "qvariant";
}

template<> std::string Attribute<QVariantList >::TypenameToString() const
{
    return "qvariantlist";
}

template<> std::string Attribute<Transform>::TypenameToString() const
{
    return "transform";
}

// FROMSTRING TEMPLATE IMPLEMENTATIONS.

template<> void Attribute<QString>::FromString(const std::string& str, AttributeChange::Type change)
{
    ///\todo decode/encode XML-risky characters
    Set(QString::fromStdString(str), change);
}

template<> void Attribute<bool>::FromString(const std::string& str, AttributeChange::Type change)
{
    std::string str_lower = str;
    boost::algorithm::to_lower(str_lower);
    bool value = (boost::algorithm::starts_with(str_lower, "true") || boost::algorithm::starts_with(str_lower, "1"));
    
    Set(value, change);
}

template<> void Attribute<int>::FromString(const std::string& str, AttributeChange::Type change)
{
    try
    {
        int value = ParseString<int>(str);
        Set(value, change);
    }
    catch (...) {}
}

template<> void Attribute<uint>::FromString(const std::string& str, AttributeChange::Type change)
{
    try
    {
        uint value = ParseString<uint>(str);
        Set(value, change);
    }
    catch (...) {}
}

template<> void Attribute<float>::FromString(const std::string& str, AttributeChange::Type change)
{
    try
    {
        float value = ParseString<float>(str);
        Set(value, change);
    }
    catch (...) {}
}

template<> void Attribute<Vector3df>::FromString(const std::string& str, AttributeChange::Type change)
{
    StringVector components = SplitString(str, ' ');
    if (components.size() == 3)
    {
        try
        {
            Vector3df value;
            value.x = ParseString<float>(components[0]);
            value.y = ParseString<float>(components[1]);
            value.z = ParseString<float>(components[2]);
            Set(value, change);
        }
        catch (...) {}
    }
}

template<> void Attribute<Color>::FromString(const std::string& str, AttributeChange::Type change)
{
    Color value;
    StringVector components = SplitString(str, ' ');
    if (components.size() == 3)
    {
        try
        {
            value.r = ParseString<float>(components[0]);
            value.g = ParseString<float>(components[1]);
            value.b = ParseString<float>(components[2]);
            Set(value, change);
        }
        catch (...) {}
    }
    if (components.size() == 4)
    {
        try
        {
            value.r = ParseString<float>(components[0]);
            value.g = ParseString<float>(components[1]);
            value.b = ParseString<float>(components[2]);
            value.a = ParseString<float>(components[3]);
            Set(value, change);
        }
        catch (...) {}
    }
}

template<> void Attribute<Quaternion>::FromString(const std::string& str, AttributeChange::Type change)
{
    StringVector components = SplitString(str, ' ');
    if (components.size() == 4)
    {
        try
        {
            Quaternion value;
            value.w = ParseString<float>(components[0]);
            value.x = ParseString<float>(components[1]);
            value.y = ParseString<float>(components[2]);
            value.z = ParseString<float>(components[3]);
            Set(value, change);
        }
        catch (...) {}
    }
}

template<> void Attribute<Foundation::AssetReference>::FromString(const std::string& str, AttributeChange::Type change)
{
    // We store type first, then ",", then asset id
    std::string::size_type pos = str.find(',');
    if (pos == std::string::npos)
        return;
    std::string type = str.substr(0, pos);
    std::string id = str.substr(pos + 1);
    
    Foundation::AssetReference value(id, type);
    Set(value, change);
}

template<> void Attribute<QVariant>::FromString(const std::string& str, AttributeChange::Type change)
{
    QVariant value(QString(str.c_str()));
    Set(value, change);
}

template<> void Attribute<QVariantList >::FromString(const std::string& str, AttributeChange::Type change)
{
    QVariantList value;
    QString strValue = QString::fromStdString(str);
    QStringList components = strValue.split(';');

    for(uint i = 0; i < components.size(); i++)
        value.push_back(QVariant(components[i]));
    if(value.size() == 1)
        if(value[0] == "")
            value.pop_back();
    Set(value, change);
}

template<> void Attribute<Transform>::FromString(const std::string& str, AttributeChange::Type change)
{
    QString value = QString::fromStdString(str);
    QStringList matrixElements = value.split(',');
    Transform result;
    if(matrixElements.size() == 9) //Ensure that we have right amount of elements.
    {
        float values[9];
        for(uint i = 0; i < 3; i++)
        {
            uint startIndex = 3 * i;
            for(uint j = 0; j < 3; j++)
                values[j + startIndex] = ParseString<float>(matrixElements[j + startIndex].toStdString(), 0.0f);
        }
        result.SetPos(values[0], values[1], values[2]);
        result.SetRot(values[3], values[4], values[5]);
        result.SetScale(values[6], values[7], values[8]);
    }
    Set(result, change);
}

// TOBINARY TEMPLATE IMPLEMENTATIONS.

template<> void Attribute<QString>::ToBinary(DataSerializer& dest) const
{
    QByteArray utf8bytes = value_.toUtf8();
    dest.Add<u16>(utf8bytes.size());
    if (utf8bytes.size())
        dest.AddArray<u8>((const u8*)utf8bytes.data(), utf8bytes.size());
}

template<> void Attribute<bool>::ToBinary(DataSerializer& dest) const
{
    if (value_)
        dest.Add<u8>(1);
    else
        dest.Add<u8>(0);
}

template<> void Attribute<int>::ToBinary(DataSerializer& dest) const
{
    dest.Add<s32>(value_);
}

template<> void Attribute<uint>::ToBinary(DataSerializer& dest) const
{
    dest.Add<u32>(value_);
}

template<> void Attribute<float>::ToBinary(DataSerializer& dest) const
{
    dest.Add<float>(value_);
}

template<> void Attribute<Vector3df>::ToBinary(DataSerializer& dest) const
{
    dest.Add<float>(value_.x);
    dest.Add<float>(value_.y);
    dest.Add<float>(value_.z);
}

template<> void Attribute<Quaternion>::ToBinary(DataSerializer& dest) const
{
    dest.Add<float>(value_.x);
    dest.Add<float>(value_.y);
    dest.Add<float>(value_.z);
    dest.Add<float>(value_.w);
}

template<> void Attribute<Color>::ToBinary(DataSerializer& dest) const
{
    dest.Add<float>(value_.r);
    dest.Add<float>(value_.g);
    dest.Add<float>(value_.b);
    dest.Add<float>(value_.a);
}

template<> void Attribute<Foundation::AssetReference>::ToBinary(DataSerializer& dest) const
{
    dest.AddString(value_.type_);
    dest.AddString(value_.id_);
}

template<> void Attribute<QVariant>::ToBinary(DataSerializer& dest) const
{
    std::string str = value_.toString().toStdString();
    dest.AddString(str);
}

template<> void Attribute<QVariantList>::ToBinary(DataSerializer& dest) const
{
    dest.Add<u8>(value_.size());
    for (uint i = 0; i < value_.size(); ++i)
    {
        std::string str = value_[i].toString().toStdString();
        dest.AddString(str);
    }
}

template<> void Attribute<Transform>::ToBinary(DataSerializer& dest) const
{
    dest.Add<float>(value_.position.x);
    dest.Add<float>(value_.position.y);
    dest.Add<float>(value_.position.z);
    dest.Add<float>(value_.rotation.x);
    dest.Add<float>(value_.rotation.y);
    dest.Add<float>(value_.rotation.z);
    dest.Add<float>(value_.scale.x);
    dest.Add<float>(value_.scale.y);
    dest.Add<float>(value_.scale.z);
}

// FROMBINARY TEMPLATE IMPLEMENTATIONS.

template<> void Attribute<QString>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    QByteArray utf8bytes;
    utf8bytes.resize(source.Read<u16>());
    if (utf8bytes.size())
        source.ReadArray<u8>((u8*)utf8bytes.data(), utf8bytes.size());
    Set(QString::fromUtf8(utf8bytes.data(), utf8bytes.size()), change);
}

template<> void Attribute<bool>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Set(source.Read<u8>() ? true : false, change);
}

template<> void Attribute<int>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Set(source.Read<s32>(), change);
}

template<> void Attribute<uint>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Set(source.Read<u32>(), change);
}

template<> void Attribute<float>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Set(source.Read<float>(), change);
}

template<> void Attribute<Vector3df>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Vector3df value;
    value.x = source.Read<float>();
    value.y = source.Read<float>();
    value.z = source.Read<float>();
    Set(value, change);
}

template<> void Attribute<Color>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Color value;
    value.r = source.Read<float>();
    value.g = source.Read<float>();
    value.b = source.Read<float>();
    value.a = source.Read<float>();
    Set(value, change);
}

template<> void Attribute<Quaternion>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Quaternion value;
    value.x = source.Read<float>();
    value.y = source.Read<float>();
    value.z = source.Read<float>();
    value.w = source.Read<float>();
    Set(value, change);
}

template<> void Attribute<Foundation::AssetReference>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Foundation::AssetReference value;
    value.type_ = source.ReadString();
    value.id_ = source.ReadString();
    Set(value, change);
}

template<> void Attribute<QVariant>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    std::string str = source.ReadString();
    QVariant value(QString(str.c_str()));
    Set(value, change);
}

template<> void Attribute<QVariantList>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    QVariantList value;
    
    u8 numValues = source.Read<u8>();
    for (u32 i = 0; i < numValues; ++i)
    {
        std::string str = source.ReadString();
        value.append(QVariant(QString(str.c_str())));
    }
    
    Set(value, change);
}

template<> void Attribute<Transform>::FromBinary(DataDeserializer& source, AttributeChange::Type change)
{
    Transform value;
    value.position.x = source.Read<float>();
    value.position.y = source.Read<float>();
    value.position.z = source.Read<float>();
    value.rotation.x = source.Read<float>();
    value.rotation.y = source.Read<float>();
    value.rotation.z = source.Read<float>();
    value.scale.x = source.Read<float>();
    value.scale.y = source.Read<float>();
    value.scale.z = source.Read<float>();
    Set(value, change);
}

// COMPAREBINARY TEMPLATE IMPLEMENTATIONS.

template<> bool Attribute<QString>::CompareBinary(DataDeserializer& source) const
{
    QByteArray utf8bytes;
    utf8bytes.resize(source.Read<u16>());
    if (utf8bytes.size())
        source.ReadArray<u8>((u8*)utf8bytes.data(), utf8bytes.size());
    
    QString value = QString::fromUtf8(utf8bytes.data(), utf8bytes.size());
    return value_ != value;
}

template<> bool Attribute<bool>::CompareBinary(DataDeserializer& source) const
{
    bool value = source.Read<u8>() ? true : false;
    return value_ != value;
}

template<> bool Attribute<int>::CompareBinary(DataDeserializer& source) const
{
    int value = source.Read<s32>();
    return value_ != value;
}

template<> bool Attribute<uint>::CompareBinary(DataDeserializer& source) const
{
    uint value = source.Read<u32>();
    return value_ != value;
}

template<> bool Attribute<float>::CompareBinary(DataDeserializer& source) const
{
    float value = source.Read<float>();
    return value_ != value;
}

template<> bool Attribute<Vector3df>::CompareBinary(DataDeserializer& source) const
{
    Vector3df value;
    value.x = source.Read<float>();
    value.y = source.Read<float>();
    value.z = source.Read<float>();
    return value_ != value;
}

template<> bool Attribute<Color>::CompareBinary(DataDeserializer& source) const
{
    Color value;
    value.r = source.Read<float>();
    value.g = source.Read<float>();
    value.b = source.Read<float>();
    value.a = source.Read<float>();
    return value_ != value;
}

template<> bool Attribute<Quaternion>::CompareBinary(DataDeserializer& source) const
{
    Quaternion value;
    value.x = source.Read<float>();
    value.y = source.Read<float>();
    value.z = source.Read<float>();
    value.w = source.Read<float>();
    return value_ != value;
}

template<> bool Attribute<Foundation::AssetReference>::CompareBinary(DataDeserializer& source) const
{
    Foundation::AssetReference value;
    value.type_ = source.ReadString();
    value.id_ = source.ReadString();
    return value_ != value;
}

template<> bool Attribute<QVariant>::CompareBinary(DataDeserializer& source) const
{
    std::string str = source.ReadString();
    QVariant value(QString(str.c_str()));
    return value_ != value;
}

template<> bool Attribute<QVariantList>::CompareBinary(DataDeserializer& source) const
{
    QVariantList value;
    
    u8 numValues = source.Read<u8>();
    for (u32 i = 0; i < numValues; ++i)
    {
        std::string str = source.ReadString();
        value.append(QVariant(QString(str.c_str())));
    }
    return value_ != value;
}

template<> bool Attribute<Transform>::CompareBinary(DataDeserializer& source) const
{
    Transform value;
    value.position.x = source.Read<float>();
    value.position.y = source.Read<float>();
    value.position.z = source.Read<float>();
    value.rotation.x = source.Read<float>();
    value.rotation.y = source.Read<float>();
    value.rotation.z = source.Read<float>();
    value.scale.x = source.Read<float>();
    value.scale.y = source.Read<float>();
    value.scale.z = source.Read<float>();
    return value_ != value;
}
